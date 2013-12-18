from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class MediaView(BrowserView):
    def setUp(self):
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()
        portal_url = portal.absolute_url()
        self.base_url = context.absolute_url()
        self.base_wurl = self.base_url + '/@@view/++widget++form.widgets.'
        self.static = portal_url + '/++resource++wildcard-media'
        self.mstatic = self.static + '/mediaelementjs'


class AudioView(MediaView):
    def __call__(self):
        self.setUp()
        self.audio_url = '%sIAudio.audio_file/@@download/%s' % (
            self.base_wurl,
            self.context.audio_file.filename
        )
        return self.index()


class VideoMacroView(MediaView):

    def __call__(self):
        context = self.context
        self.setUp()

        self.base_furl = self.base_wurl + 'IVideo.'
        self.videos = []
        for (_type, fieldname) in (('mp4', 'video_file'),
                                   ('ogg', 'video_file_ogv'),
                                   ('webm', 'video_file_webm')):
            file = getattr(context, fieldname, None)
            if file:
                self.videos.append({
                    'type': _type,
                    'url': '%svideo_file/@@download/%s' % (
                        self.base_furl,
                        file.filename)
                })
        if self.videos:
            self.mp4_url = self.videos[0]['url']
        else:
            self.mp4_url = None
        image = self.context.image
        if image:
            self.image_url = '%s/@@images/image' % (
                self.base_url
            )
        else:
            self.image_url = None
        subtitles = self.context.subtitle_file
        if subtitles:
            self.subtitles_url = '%ssubtitle_file/@@download/%s' % (
                self.base_furl,
                subtitles.filename
            )
        else:
            self.subtitles_url = None

        self.width = getattr(context, 'width', 640)
        self.height = getattr(context, 'height', 320)
        return self.index()
