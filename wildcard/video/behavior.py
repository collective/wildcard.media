# -*- coding: utf-8 -*-
from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.supermodel import model
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as namedfile
from wildcard.video import _
from wildcard.video.async import queueJob
from zope.interface import Invalid
import json
from plone.directives import form


def valid_video(namedblob):
    if namedblob.contentType.split('/')[0] != 'video':
        raise Invalid("must be a video file")
    return True


class IVideo(model.Schema):

    image = namedfile.NamedBlobImage(
        title=_(u"Cover Image"),
        description=u"",
        required=False,
    )

    # main file will always be converted to mp4
    video_file = namedfile.NamedBlobFile(
        title=_(u"Video File"),
        description=u"",
        required=False,
        constraint=valid_video
    )

    form.omitted('video_file_ogv')
    video_file_ogv = namedfile.NamedBlobFile(
        required=False,
    )

    form.omitted('video_file_webm')
    video_file_webm = namedfile.NamedBlobFile(
        required=False,
    )

    youtube_url = schema.TextLine(
        title=_(u"Youtube URL"),
        description=_(u"Alternatively, you can provide a youtube video url. "
                      u"If this is specified, video file will be ignored."),
        required=False
    )

    width = schema.Int(
        title=_(u"Width"),
        default=640
    )

    height = schema.Int(
        title=_(u"Height"),
        default=320
    )

    form.omitted('metadata')
    metadata = schema.Text(
        required=False
    )


alsoProvides(IVideo, IFormFieldProvider)


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


class Video(object):
    implements(IVideo)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    def _get_video_file(self):
        return self.context.video_file

    def _set_video_file(self, value):
        if value != self.context.video_file:
            self.context.video_file = value
            queueJob(self.context)
    video_file = property(_get_video_file, _set_video_file)

    def _get_metadata(self):
        return unicode(json.dumps(getattr(self.context, 'metadata', {})))

    def _set_metadata(self, value):
        pass

    metadata = property(_get_metadata, _set_metadata)

    image = BasicProperty(IVideo['image'])
    youtube_url = BasicProperty(IVideo['youtube_url'])
    width = BasicProperty(IVideo['width'])
    height = BasicProperty(IVideo['height'])

    video_file_ogv = UnsettableProperty(IVideo['video_file_ogv'])
    video_file_webm = UnsettableProperty(IVideo['video_file_webm'])
