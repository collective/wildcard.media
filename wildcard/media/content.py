from wildcard.media.interfaces import IAudioEnabled, IVideoEnabled
from plone.dexterity.content import Item
from zope.interface import implements


class Audio(Item):
    implements(IAudioEnabled)


class Video(Item):
    implements(IVideoEnabled)
