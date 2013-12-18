from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class VideoView(BrowserView):
    def has_video(self):
        if self.context.video_file:
            return True
        return False

    def __call__(self):
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()
        portal_url = portal.absolute_url()
        self.base_url = context.absolute_url()
        self.base_furl = self.base_url + '/@@view/++widget++form.widgets.IVideo.'
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
        self.static = portal_url + '/++resource++wildcard-video'
        self.mstatic = self.static + '/mediaelementjs'
        image = self.context.image
        if image:
            self.image_url = '%simage/@@download/%s' % (
                self.base_furl,
                image.filename
            )
        else:
            self.image_url = None
        self.width = getattr(context, 'width', 640)
        self.height = getattr(context, 'height', 320)
        return self.index()
