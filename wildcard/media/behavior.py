# -*- coding: utf-8 -*-
from zope.interface import alsoProvides, implements
from zope.component import adapts
from z3c.form.interfaces import IAddForm, IEditForm
from zope import schema
from plone.supermodel import model
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as namedfile
from wildcard.media import _
from wildcard.media.async import queueJob
from wildcard.media.widget import StreamNamedFileFieldWidget
from zope.interface import Invalid, invariant
import json
from plone.autoform import directives as form
from plone.app.textfield import RichText


def valid_video(namedblob):
    if namedblob.contentType.split('/')[0] != 'video':
        raise Invalid("must be a video file")
    return True


def valid_audio(namedblob):
    if namedblob.contentType.split('/')[0] != 'audio':
        raise Invalid("must be a audio file")
    return True


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
                      u"If this is specified, video file will be ignored."),
        required=False
    )

    @invariant
    def validate_videos(data):
        if not data.video_file and not data.youtube_url:
            raise Invalid("Must specify either a video file or youtube url")

    width = schema.Int(
        title=_(u"Width"),
        default=640
    )

    height = schema.Int(
        title=_(u"Height"),
        default=320
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

    def _get_video_file(self):
        return self.context.video_file

    def _set_video_file(self, value):
        if value is None:
            self.context.video_file = None
            self.context.video_file_ogv = None
            self.context.video_file_webm = None
        elif value != getattr(self.context, 'video_file', _marker):
            self.context.video_file = value
            queueJob(self.context)
    video_file = property(_get_video_file, _set_video_file)

    image = BasicProperty(IVideo['image'])
    youtube_url = BasicProperty(IVideo['youtube_url'])
    width = BasicProperty(IVideo['width'])
    height = BasicProperty(IVideo['height'])
    transcript = BasicProperty(IVideo['transcript'])
    subtitle_file = BasicProperty(IVideo['subtitle_file'])

    video_file_ogv = UnsettableProperty(IVideo['video_file_ogv'])
    video_file_webm = UnsettableProperty(IVideo['video_file_webm'])
    image = UnsettableProperty(IVideo['image'])


class Audio(BaseAdapter):
    implements(IAudio)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    audio_file = BasicProperty(IAudio['audio_file'])
    transcript = BasicProperty(IAudio['transcript'])
