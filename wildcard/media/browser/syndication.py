from Products.CMFPlone.browser.syndication.adapters import DexterityItem
from Products.CMFPlone.interfaces.syndication import IFeed
from zope.component import adapts
from wildcard.media.interfaces import IAudioEnabled, IVideoEnabled
from zope.cachedescriptors.property import Lazy as lazy_property


class AudioFeedItem(DexterityItem):
    adapts(IAudioEnabled, IFeed)

    @property
    def has_enclosure(self):
        return True

    @property
    def file_url(self):
        return '%s/@@download/audio_file/%s' % (
            self.base_url,
            self.context.audio_file.filename
        )

    @lazy_property
    def file(self):
        return self.context.audio_file


class VideoFeedItem(DexterityItem):
    adapts(IVideoEnabled, IFeed)

    @property
    def file_url(self):
        url = self.base_url

        fi = self.file
        if fi is not None:
            filename = fi.filename
            if filename:
                url += '/@@download/video_file/%s' % filename
        return url

    @property
    def has_enclosure(self):
        if self.context.video_file:
            return True
        return False

    @lazy_property
    def file(self):
        if self.has_enclosure:
            return self.context.video_file
