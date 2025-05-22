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
    VIDEO_FORMATS_VOCAB.append(SimpleTerm(format.type_, format.type_, format.name))


class IGlobalMediaSettings(Interface):
    additional_video_formats = schema.List(
        title=_("Additional Video Formats"),
        description=_(
            "additional_video_formats_help",
            default="To provide better HTML5 support, different video "
            "formats are generated via avconv (formerly ffmpeg). "
            "If you'd prefer to save on disc space, but provide "
            "less HTML5 support, change the additional video "
            "formats that are generated here",
        ),
        default=["ogg", "webm"],
        value_type=schema.Choice(vocabulary=SimpleVocabulary(VIDEO_FORMATS_VOCAB)),
    )
    async_quota_size = schema.Int(
        title=_("Async Quota Size"),
        description=_(
            "Number of conversions to run at a time. "
            "The quota name assigned is `wildcard.media`."
        ),
        default=3,
    )

    force = schema.Bool(
        title=_("Force video conversion"),
        description=_(
            "always_convert_help",
            default="Force the video through the full conversion "
            "process, even if it is already in the final video format."
            " This may be useful if you always want to transcode to a "
            "given video size.",
        ),
        default=False,
    )

    avconv_in_mp4 = schema.TextLine(
        title=_("MP4: infile parameters"),
        description=_(
            "avconv_in_mp4_help",
            default="Pass optional infile parameters to aconv during the "
            "MP4 conversion process.",
        ),
        default="",
        required=False,
    )

    avconv_out_mp4 = schema.TextLine(
        title=_("MP4: outfile parameters"),
        description=_(
            "avconv_out_mp4_help",
            default="Pass optional outfile parameters to aconv during the "
            "MP4 conversion process.",
        ),
        default="",
        required=False,
    )

    avconv_in_webm = schema.TextLine(
        title=_("WebM: infile parameters"),
        description=_(
            "avconv_in_webm_help",
            default="Pass optional infile parameters to aconv during the "
            "WebM conversion process.",
        ),
        default="",
        required=False,
    )

    avconv_out_webm = schema.TextLine(
        title=_("WebM: outfile parameters"),
        description=_(
            "avconv_out_webm_help",
            default="Pass optional outfile parameters to aconv during the "
            "WebM conversion process.",
        ),
        default="",
        required=False,
    )

    avconv_in_ogg = schema.TextLine(
        title=_("OGG: infile parameters"),
        description=_(
            "avconv_in_ogg_help",
            default="Pass optional infile parameters to aconv during the "
            "OGG conversion process.",
        ),
        default="",
        required=False,
    )

    avconv_out_ogg = schema.TextLine(
        title=_("OGG: outfile parameters"),
        description=_(
            "avconv_out_ogg_help",
            default="Pass optional outfile parameters to aconv during the "
            "OGG conversion process.",
        ),
        default="",
        required=False,
    )

    default_video_width = schema.Int(title=_("Default video width"), default=720)

    default_video_height = schema.Int(title=_("Default video height"), default=400)


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


class IVideoEmbedCode(Interface):
    """Marker interface to provide a video embed html code"""
