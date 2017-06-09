# -*- coding: utf-8 -*-

from wildcard.media.interfaces import IVideoEnabled
from zope.interface import implements
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile


class VideoEmbedCode(object):

    implements(IVideoEnabled)
    template = ViewPageTemplateFile('templates/internalvideo_template.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return self.template()
