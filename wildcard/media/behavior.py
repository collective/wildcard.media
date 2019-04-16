# -*- coding: utf-8 -*-
import json
import re

from plone.app.textfield import RichText
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field as namedfile
from plone.supermodel import model
from wildcard.media import _
from wildcard.media.browser.widget import StreamNamedFileFieldWidget
from wildcard.media.settings import GlobalSettings
from z3c.form.interfaces import IAddForm, IEditForm
from zope import schema
from zope.component import adapts
from zope.component.hooks import getSite
from zope.interface import alsoProvides, implements
from zope.interface import Invalid, invariant

try:
    from wildcard.media import youtube
except ImportError:
    youtube = None


def valid_video(namedblob):
    if namedblob.contentType.split('/')[0] != 'video':
        raise Invalid("must be a video file")
    return True


def valid_audio(namedblob):
    if namedblob.contentType.split('/')[0] != 'audio':
        raise Invalid("must be a audio file")
    return True


def getDefaultWidth():
    portal = getSite()
    settings = GlobalSettings(portal)
    return settings.default_video_width


def getDefaultHeight():
    portal = getSite()
    settings = GlobalSettings(portal)
    return settings.default_video_height


class IVideo(model.Schema):

    form.omitted('image')
    image = namedfile.NamedBlobImage(
        title=_(u"Cover Image"),
        description=u"",
        required=False,
    )

    # main file will always be converted to mp4
    form.widget(video_file=StreamNamedFileFieldWidget)
    model.primary('video_file')
    video_file = namedfile.NamedBlobFile(
        title=_(u"Video File"),
        description=u"",
        required=False,
        constraint=valid_video
    )

    if youtube:
        upload_video_to_youtube = schema.Bool(
            title=_(u'Upload to youtube'),
            description=_(u'Requires having youtube account connected. '
                          u'Videos that are private will remain unlisted on YouTube. '
                          u'Once published, video will be made public on YouTube. '),
            required=False,
            default=False)

    form.omitted(IAddForm, 'video_file_ogv')
    form.omitted(IEditForm, 'video_file_ogv')
    form.widget(video_file_ogv=StreamNamedFileFieldWidget)
    video_file_ogv = namedfile.NamedBlobFile(
        required=False,
    )

    form.omitted(IAddForm, 'video_file_webm')
    form.omitted(IEditForm, 'video_file_webm')
    form.widget(video_file_webm=StreamNamedFileFieldWidget)
    video_file_webm = namedfile.NamedBlobFile(
        required=False,
    )

    youtube_url = schema.TextLine(
        title=_(u"Youtube URL"),
        description=_(u"Alternatively, you can provide a youtube video url. "
                      u"If this is specified, video file will be ignored. "
                      u"If video was uploaded to youtube, this field will be filled "
                      u"with video url."),
        required=False
    )
    retrieve_thumb = schema.Bool(
        title=_(u'Retrieve original thumbnail from youtube'),
        description=_(u"If checked, try to download original thumbnail from "
                      u"youtube into this video."),
        required=False,
        default=False)

    @invariant
    def validate_videos(data):
        if not data.video_file and not data.youtube_url:
            raise Invalid("Must specify either a video file or youtube url")

    width = schema.Int(
        title=_(u"Width"),
        defaultFactory=getDefaultWidth
    )

    height = schema.Int(
        title=_(u"Height"),
        defaultFactory=getDefaultHeight
    )

    subtitle_file = namedfile.NamedBlobFile(
        title=_(u"Subtitle file"),
        description=_(u"Provide a file in srt format"),
        required=False
    )

    form.omitted('metadata')
    metadata = schema.Text(
        required=False
    )

    transcript = RichText(
        title=_(u"Transcript"),
        default_mime_type='text/html',
        output_mime_type='text/html',
        allowed_mime_types=('text/html', 'text/plain'),
        default=u"",
        required=False
    )


alsoProvides(IVideo, IFormFieldProvider)



class IAudio(model.Schema):

    # main file will always be converted to mp4
    form.widget(audio_file=StreamNamedFileFieldWidget)
    model.primary('audio_file')
    audio_file = namedfile.NamedBlobFile(
        title=_(u"Audio File"),
        description=u"",
        required=True,
        constraint=valid_audio
    )

    form.omitted('metadata')
    metadata = schema.Text(
        required=False
    )

    transcript = RichText(
        title=_(u"Transcript"),
        default_mime_type='text/html',
        output_mime_type='text/html',
        allowed_mime_types=('text/html', 'text/plain'),
        default=u"",
        required=False
    )

alsoProvides(IAudio, IFormFieldProvider)

class IVideoOptional(model.Schema):

    form.omitted('image')
    image = namedfile.NamedBlobImage(
        title=_(u"Cover Image"),
        description=u"",
        required=False,
    )

    # main file will always be converted to mp4
    form.widget(video_file=StreamNamedFileFieldWidget)
    model.primary('video_file')
    video_file = namedfile.NamedBlobFile(
        title=_(u"Video File"),
        description=u"",
        required=False,
        constraint=valid_video
    )

    if youtube:
        upload_video_to_youtube = schema.Bool(
            title=_(u'Upload to youtube'),
            description=_(u'Requires having youtube account connected. '
                          u'Videos that are private will remain unlisted on YouTube. '
                          u'Once published, video will be made public on YouTube. '),
            required=False,
            default=False)

    form.omitted(IAddForm, 'video_file_ogv')
    form.omitted(IEditForm, 'video_file_ogv')
    form.widget(video_file_ogv=StreamNamedFileFieldWidget)
    video_file_ogv = namedfile.NamedBlobFile(
        required=False,
    )

    form.omitted(IAddForm, 'video_file_webm')
    form.omitted(IEditForm, 'video_file_webm')
    form.widget(video_file_webm=StreamNamedFileFieldWidget)
    video_file_webm = namedfile.NamedBlobFile(
        required=False,
    )

    youtube_url = schema.TextLine(
        title=_(u"Youtube URL"),
        description=_(u"Alternatively, you can provide a youtube video url. "
                      u"If this is specified, video file will be ignored. "
                      u"If video was uploaded to youtube, this field will be filled "
                      u"with video url."),
        required=False
    )
    retrieve_thumb = schema.Bool(
        title=_(u'Retrieve original thumbnail from youtube'),
        description=_(u"If checked, try to download original thumbnail from "
                      u"youtube into this video."),
        required=False,
        default=False)

    width = schema.Int(
        title=_(u"Width"),
        defaultFactory=getDefaultWidth
    )

    height = schema.Int(
        title=_(u"Height"),
        defaultFactory=getDefaultHeight
    )

    subtitle_file = namedfile.NamedBlobFile(
        title=_(u"Subtitle file"),
        description=_(u"Provide a file in srt format"),
        required=False
    )

    form.omitted('metadata')
    metadata = schema.Text(
        required=False
    )

    transcript = RichText(
        title=_(u"Transcript"),
        default_mime_type='text/html',
        output_mime_type='text/html',
        allowed_mime_types=('text/html', 'text/plain'),
        default=u"",
        required=False
    )


alsoProvides(IVideoOptional, IFormFieldProvider)


class IAudioOptional(IAudio):

    # main file will always be converted to mp4
    form.widget(audio_file=StreamNamedFileFieldWidget)
    model.primary('audio_file')
    audio_file = namedfile.NamedBlobFile(
        title=_(u"Audio File"),
        description=u"",
        required=False,
        constraint=valid_audio
    )

    form.omitted('metadata')
    metadata = schema.Text(
        required=False
    )

    transcript = RichText(
        title=_(u"Transcript"),
        default_mime_type='text/html',
        output_mime_type='text/html',
        allowed_mime_types=('text/html', 'text/plain'),
        default=u"",
        required=False
    )

alsoProvides(IAudioOptional, IFormFieldProvider)


class UnsettableProperty(object):
    """
    Property that can not be saved from a form
    """

    def __init__(self, field):
        self._field = field

    def __get__(self, inst, klass):
        if inst is None:
            return self
        return getattr(inst.context, self._field.__name__, self._field.default)

    def __set__(self, inst, value):
        pass

    def __getattr__(self, name):
        return getattr(self._field, name)


class BasicProperty(object):

    def __init__(self, field):
        self._field = field

    def __get__(self, inst, klass):
        if inst is None:
            return self
        return getattr(inst.context, self._field.__name__, self._field.default)

    def __set__(self, inst, value):
        setattr(inst.context, self._field.__name__, value)

    def __getattr__(self, name):
        return getattr(self._field, name)


class BaseAdapter(object):

    def _get_metadata(self):
        return unicode(json.dumps(getattr(self.context, 'metadata', {})))

    def _set_metadata(self, value):
        pass

    metadata = property(_get_metadata, _set_metadata)


_marker = object()


class Video(BaseAdapter):
    implements(IVideo)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    # For when a fileUpload sends us a file
    def _get_file(self):
        return self.context.video_file

    def _set_file(self, value):
        self.video_file = value
    file = property(_get_file, _set_file)

    def _get_video_file(self):
        return self.context.video_file

    def _set_video_file(self, value):
        if value is None:
            self.context.video_file = None
            self.context.video_file_ogv = None
            self.context.video_file_webm = None
        elif value != getattr(self.context, 'video_file', _marker):
            self.context.video_converted = False
            self.context.video_file = value

    def get_youtube_id_from_url(self):
        if not getattr(self.context, 'youtube_url', None):
            return ""
        pattern = r"((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"
        match = re.search(pattern, self.context.youtube_url)
        if not match:
            return ""
        return match.group()

    video_file = property(_get_video_file, _set_video_file)

    image = BasicProperty(IVideo['image'])
    youtube_url = BasicProperty(IVideo['youtube_url'])
    retrieve_thumb = BasicProperty(IVideo['retrieve_thumb'])
    width = BasicProperty(IVideo['width'])
    height = BasicProperty(IVideo['height'])
    transcript = BasicProperty(IVideo['transcript'])
    subtitle_file = BasicProperty(IVideo['subtitle_file'])

    video_file_ogv = UnsettableProperty(IVideo['video_file_ogv'])
    video_file_webm = UnsettableProperty(IVideo['video_file_webm'])
    image = UnsettableProperty(IVideo['image'])

    if youtube:
        upload_video_to_youtube = BasicProperty(IVideo['upload_video_to_youtube'])

class VideoOptional(Video):
    implements(IVideoOptional)
    adapts(IVideo)

    def __init__(self, context):
        self.context = context

    # For when a fileUpload sends us a file
    def _get_file(self):
        return self.context.video_file

    def _set_file(self, value):
        self.video_file = value
    file = property(_get_file, _set_file)

    def _get_video_file(self):
        return self.context.video_file

    def _set_video_file(self, value):
        if value is None:
            self.context.video_file = None
            self.context.video_file_ogv = None
            self.context.video_file_webm = None
        elif value != getattr(self.context, 'video_file', _marker):
            self.context.video_converted = False
            self.context.video_file = value

    def get_youtube_id_from_url(self):
        if not getattr(self.context, 'youtube_url', None):
            return ""
        pattern = r"((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"
        match = re.search(pattern, self.context.youtube_url)
        if not match:
            return ""
        return match.group()

    video_file = property(_get_video_file, _set_video_file)

    image = BasicProperty(IVideo['image'])
    youtube_url = BasicProperty(IVideo['youtube_url'])
    retrieve_thumb = BasicProperty(IVideo['retrieve_thumb'])
    width = BasicProperty(IVideo['width'])
    height = BasicProperty(IVideo['height'])
    transcript = BasicProperty(IVideo['transcript'])
    subtitle_file = BasicProperty(IVideo['subtitle_file'])

    video_file_ogv = UnsettableProperty(IVideo['video_file_ogv'])
    video_file_webm = UnsettableProperty(IVideo['video_file_webm'])
    image = UnsettableProperty(IVideo['image'])

    if youtube:
        upload_video_to_youtube = BasicProperty(IVideo['upload_video_to_youtube'])


class Audio(BaseAdapter):
    implements(IAudio)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    audio_file = BasicProperty(IAudio['audio_file'])
    transcript = BasicProperty(IAudio['transcript'])

class AudioOptional(Audio):
    implements(IAudioOptional)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    audio_file = BasicProperty(IAudioOptional['audio_file'])
    transcript = BasicProperty(IAudioOptional['transcript'])
