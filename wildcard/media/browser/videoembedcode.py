# -*- coding: utf-8 -*-

from zope.interface import Interface

class VideoEmbedCode(Interface):

    def __call__(self):
        return "<h1> CIAO! </h1>"
