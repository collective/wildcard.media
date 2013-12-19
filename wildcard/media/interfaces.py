from zope.interface import Interface
from zope import schema
from wildcard.media import _
from wildcard.media.config import CONVERTABLE_FORMATS
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class IMediaEnabled(Interface):
    pass


class IAudioEnabled(IMediaEnabled):
    pass


class IVideoEnabled(IMediaEnabled):
    pass


class ILayer(Interface):
    pass


VIDEO_FORMATS_VOCAB = []

for format in CONVERTABLE_FORMATS:
    VIDEO_FORMATS_VOCAB.append(
        SimpleTerm(format.type_, format.type_, format.name))


class IGlobalMediaSettings(Interface):
    additional_video_formats = schema.List(
        title=_("Additional Video Formats"),
        description=_(u"To provide better HTML5 support, different video "
                      u"formats are generated via avconv(formerly ffmpeg). "
                      u"If you'd prefer to save on disc space, but provide "
                      u"less HTML5 support, change the additional video "
                      u"formats that are generated here"),
        default=['ogg', 'webm'],
        value_type=schema.Choice(
            vocabulary=SimpleVocabulary(VIDEO_FORMATS_VOCAB)
        )
    )
    async_quota_size = schema.Int(
        title=_("Async Quota Size"),
        description=_("Number of conversions to run at a time. "
                      "The quota name assigned is `wildcard.media`."),
        default=3)


class IUtils(Interface):
    def valid_type(self):
        pass
