from persistent.dict import PersistentDict
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from wildcard.media.interfaces import IGlobalMediaSettings


class Base(object):
    use_interface = None

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)

        self._metadata = annotations.get('wildcard.media', None)
        if self._metadata is None:
            self._metadata = PersistentDict()
            annotations['wildcard.media'] = self._metadata

    def __setattr__(self, name, value):
        if name[0] == '_' or name in ['context', 'use_interface']:
            self.__dict__[name] = value
        else:
            self._metadata[name] = value

    def __getattr__(self, name):
        default = None
        if name in self.use_interface.names():
            default = self.use_interface[name].default

        return self._metadata.get(name, default)


class GlobalSettings(Base):
    use_interface = IGlobalMediaSettings
    implements(IGlobalMediaSettings)
