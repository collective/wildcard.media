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
        description=_('additional_video_formats_help',
                      default=u"To provide better HTML5 support, different video "
                              u"formats are generated via avconv (formerly ffmpeg). "
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

    convert_infile_options = schema.TextLine(
        title=_("Convert Infile Options"),
        description=_(
            'convert_infile_options_help',
            default=u"Pass optional infile parameters to aconv during the "
                    u"conversion process.\n"
        ),
        default=u'',
        required=False,
    )

    convert_outfile_options = schema.TextLine(
        title=_("Convert Outfile Options"),
        description=_(
            'convert_outfile_options_help',
            default=u"Pass optional outfile parameters to aconv during the "
                    u"conversion process."
        ),
        default=u'',
        required=False,
    )

    default_video_width = schema.Int(
        title=_(u'Default video width'),
        default=720)

    default_video_height = schema.Int(
        title=_(u'Default video height'),
        default=400)


class IUtils(Interface):
    def valid_type(self):
        pass

    def videos(self):
        pass

    def mp4_url(self):
        pass

    def image_url(self):
        pass

    def mp4_url_quoted(self):
        pass

    def image_url_quoted(self):
        pass

    def settings(self):
        pass
