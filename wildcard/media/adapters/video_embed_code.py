# -*- coding: utf-8 -*-
from wildcard.media.behavior import IVideo
from wildcard.media.interfaces import IVideoEmbedCode
from wildcard.media.interfaces import IVideoEnabled
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from wildcard.media.interfaces import IVideoEnabled
from zope.interface import Interface
from zope.component import adapter

try:
    # Python 3
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


@implementer(IVideoEmbedCode)
@adapter(IVideoEnabled, Interface)
class BaseEmbedCode:
    template = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return self.template()


class DefaultVideoEmbedCode(BaseEmbedCode):
    """"""

    template = ViewPageTemplateFile("templates/default_template.pt")


class InternalVideoEmbedCode(BaseEmbedCode):
    """Internal video adapter"""

    template = ViewPageTemplateFile("templates/internal_video_template.pt")


class YoutubeVideoEmbedCode(BaseEmbedCode):
    """
    Provides a way to have the html code to embed Youtube video in a web page
    """

    template = ViewPageTemplateFile("templates/youtube_embed_template.pt")

    def get_video_link(self):
        qs = urlparse(self.context.getRemoteUrl())[4]
        params = qs.split("&")
        for param in params:
            k, v = param.split("=")
            if k == "v":
                return "https://www.youtube.com/embed/{}".format(v)

    def get_embed_video_link(self):
        """Video link, just for embedding needs"""
        return self.get_video_link()

    def get_video_id(self, parsed_remote_url):
        qs = parsed_remote_url[4]
        return dict([x.split("=") for x in qs.split("&")])["v"]

    def get_embed_url(self):
        """
        Try to guess video id from a various case of possible youtube urls and
        returns the correct url for embed.
        For example:
        - 'https://youtu.be/VIDEO_ID'
        - 'https://www.youtube.com/watch?v=VIDEO_ID'
        - 'https://www.youtube.com/embed/2Lb2BiUC898'
        """
        video_behavior = IVideo(self.context)
        if not video_behavior:
            return ""
        video_id = video_behavior.get_youtube_id_from_url()
        if not video_id:
            return ""
        return "https://www.youtube.com/embed/" + video_id + "?rel=0"
