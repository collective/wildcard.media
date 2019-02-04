from wildcard.media.interfaces import IAudioEnabled, IVideoEnabled
from plone.dexterity.content import Item
from zope.interface import implementer


@implementer(IAudioEnabled)
class Audio(Item):
    pass


@implementer(IVideoEnabled)
class Video(Item):
    pass
