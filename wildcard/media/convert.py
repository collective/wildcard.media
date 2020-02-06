try:
    from zope.app.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite
import subprocess
import os
from logging import getLogger
from tempfile import mkdtemp
from shutil import copyfile, rmtree
import shlex
from wildcard.media.config import getFormat
from plone.namedfile import NamedBlobFile, NamedBlobImage
from wildcard.media.settings import GlobalSettings
from Products.CMFCore.utils import getToolByName
import six

logger = getLogger('wildcard.media')


class BaseSubProcess(object):
    default_paths = ['/bin', '/usr/bin', '/usr/local/bin']
    bin_name = ''

    if os.name == 'nt':
        close_fds = False
    else:
        close_fds = True

    def __init__(self):
        binary = self._findbinary()
        self.binary = binary
        if binary is None:
            raise IOError("Unable to find %s binary" % self.bin_name)

    def _findbinary(self):
        if 'PATH' in os.environ:
            path = os.environ['PATH']
            path = path.split(os.pathsep)
        else:
            path = self.default_paths

        for directory in path:
            fullname = os.path.join(directory, self.bin_name)
            if os.path.exists(fullname):
                return fullname

        return None

    def _run_command(self, cmd, or_error=False):
        if isinstance(cmd, six.string_types):
            cmd = cmd.split()
        cmdformatted = ' '.join(cmd)
        logger.info("Running command %s" % cmdformatted)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   close_fds=self.close_fds)
        output, error = process.communicate()
        process.stdout.close()
        process.stderr.close()
        if process.returncode != 0:
            error = """Command
%s
finished with return code
%i
and output:
%s
%s""" % (cmdformatted, process.returncode, output, error)
            logger.info(error)
            raise Exception(error)
        logger.info("Finished Running Command %s" % cmdformatted)
        if not output:
            if or_error:
                return error
        return output


class AVConvProcess(BaseSubProcess):
    """
    """
    if os.name == 'nt':
        bin_name = 'avconv.exe'
    else:
        bin_name = 'avconv'

    def convert(self, filepath, outputfilepath, video_type, video):
        portal = getSite()
        settings = GlobalSettings(portal)

        params = self.get_avconv_params(settings, video_type, video)

        cmd = [self.binary] + params['in'] + ['-i', filepath] + params['out'] + [outputfilepath]

        self._run_command(cmd)

    def grab_frame(self, filepath, outputfilepath, instant='00:00:5'):
        cmd = [self.binary, '-i', filepath, '-ss', instant, '-f', 'image2',
               '-vframes', '1', outputfilepath]
        self._run_command(cmd)

    def get_avconv_params(self, settings, video_type, video):
        params = {}
        for op in ('in', 'out'):
            option = getattr(settings, 'avconv_%s_%s' % (op, video_type)) or ''
            # replace width/height if set
            option = option.replace('{width}', str(video.width))
            option = option.replace('{height}', str(video.height))
            params[op] = shlex.split(option)
        return params

try:
    avconv = AVConvProcess()
except IOError:
    avconv = None
    logger.warning('ffmpeg not installed. wildcard.video will not function')


class AVProbeProcess(BaseSubProcess):
    """
    """
    if os.name == 'nt':
        bin_name = 'avprobe.exe'
    else:
        bin_name = 'avprobe'

    def info(self, filepath):
        cmd = [self.binary, filepath]
        result = {}
        for line in self._run_command(cmd, or_error=True).splitlines():
            if ':' not in line:
                continue
            name, data = line.split(':', 1)
            data = data.strip()
            if not data:
                continue
            name = name.strip().lower()
            if ' ' in name:
                continue
            result[name] = data
        return result

try:
    avprobe = AVProbeProcess()
except IOError:
    avprobe = None
    logger.warning('avprobe not installed. wildcard.video will not function')


def switchFileExt(filename, ext):
    filebase = filename.rsplit('.', 1)[0]
    return filebase + '.' + ext


def _convertFormat(context):
    # reset these...
    context.video_file_ogv = None
    context.video_file_webm = None

    video = context.video_file
    context.video_converted = True
    try:
        opened = video._blob.open('r')
        bfilepath = opened.name
        opened.close()
    except IOError:
        logger.warning('error opening blob file')
        return

    tmpdir = mkdtemp()
    tmpfilepath = os.path.join(tmpdir, video.filename)
    copyfile(bfilepath, tmpfilepath)

    try:
        metadata = avprobe.info(tmpfilepath)
    except:
        logger.warning('not a valid video format')
        return
    context.metadata = metadata

    conversion_types = {
        'mp4': 'video_file'
    }

    portal = getToolByName(context, 'portal_url').getPortalObject()
    settings = GlobalSettings(portal)
    for type_ in settings.additional_video_formats:
        format = getFormat(type_)
        if format:
            conversion_types[format.extension] = 'video_file_%s' % (
                format.extension
            )

    # sometimes force full video conversion
    force = settings.force

    for video_type, fieldname in conversion_types.items():
        if video_type == video.contentType.split('/')[-1] and not force:
            setattr(context, fieldname, video)
        else:
            output_filepath = os.path.join(tmpdir, 'output.' + video_type)
            try:
                avconv.convert(tmpfilepath, output_filepath, video_type, context)
            except:
                logger.warning('error converting to %s' % video_type)
                continue
            if os.path.exists(output_filepath):
                fi = open(output_filepath)
                namedblob = NamedBlobFile(
                    fi, filename=switchFileExt(video.filename,  video_type))
                setattr(context, fieldname, namedblob)
                fi.close()

    # try and grab one from video
    output_filepath = os.path.join(tmpdir, u'screengrab.png')
    try:
        avconv.grab_frame(tmpfilepath, output_filepath)
        if os.path.exists(output_filepath):
            with open(output_filepath, 'rb') as fi:
                data = fi.read()
            context.image = NamedBlobImage(data, filename=u'screengrab.png')
            fi.close()
    except:
        logger.warning('error getting thumbnail from video')
    rmtree(tmpdir)


def convertVideoFormats(context):
    if not avprobe or not avconv:
        logger.warning('can not run wildcard.media conversion. No avconv')
        return
    _convertFormat(context)
