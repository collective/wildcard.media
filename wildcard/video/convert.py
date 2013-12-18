import subprocess
import os
from logging import getLogger
from plone.app.blob.utils import openBlob
from tempfile import mkdtemp
from shutil import copyfile, rmtree
from plone.namedfile import NamedBlobFile
logger = getLogger('wildcard.video')


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
        if isinstance(cmd, basestring):
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

    def convert(self, filepath, outputfilepath):
        cmd = [self.binary, '-i', filepath, outputfilepath]
        self._run_command(cmd)

try:
    avconv = AVConvProcess()
except IOError:
    avconv = None
    logger.warn('ffmpeg not installed. wildcard.video will not function')


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
    logger.warn('avprobe not installed. wildcard.video will not function')


conversion_types = {
    'mp4': 'video_file',
    'ogv': 'video_file_ogv',
    'webm': 'video_file_webm'
}


def switchFileExt(filename, ext):
    filebase = filename.rsplit('.', 1)[0]
    return filebase + '.' + ext


def runConversion(context):
    if not avprobe or not avconv:
        logger.warn('can not run wildcard.video conversion. No avconv')
        return
    video = context.video_file
    try:
        opened = openBlob(video._blob)
        bfilepath = opened.name
        opened.close()
    except IOError:
        logger.warn('error opening blob file')
        return

    tmpdir = mkdtemp()
    tmpfilepath = os.path.join(tmpdir, video.filename)
    copyfile(bfilepath, tmpfilepath)

    try:
        metadata = avprobe.info(tmpfilepath)
    except:
        logger.warn('not a valid video format')
        return
    context.metadata = metadata

    for video_type, fieldname in conversion_types.items():
        if video_type == video.contentType.split('/')[-1]:
            setattr(context, fieldname, video)
        else:
            output_filepath = os.path.join(tmpdir, 'output.' + video_type)
            try:
                avconv.convert(tmpfilepath, output_filepath)
            except:
                logger.warn('error converting to %s' % video_type)
                continue
            if os.path.exists(output_filepath):
                namedblob = NamedBlobFile(
                    output_filepath,
                    filename=switchFileExt(video.filename,  video_type))
                setattr(context, fieldname, namedblob)

    rmtree(tmpdir)
