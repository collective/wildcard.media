from persistent.dict import PersistentDict
from zope.interface import implementer
from zope.annotation.interfaces import IAnnotations
from wildcard.media.interfaces import IGlobalMediaSettings


class Base(object):
    use_interface = None

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)

        self._metadata = annotations.get('wildcard.media', None)

    def __setattr__(self, name, value):
        if name[0] == '_' or name in ['context', 'use_interface']:
            self.__dict__[name] = value
        else:
            if self._metadata is None:
                self._metadata = PersistentDict()
                annotations = IAnnotations(self.context)
                annotations['wildcard.media'] = self._metadata
            self._metadata[name] = value

    def __getattr__(self, name):
        default = None
        if name in self.use_interface.names():
            default = self.use_interface[name].default

        if self._metadata is None:
            return default
        return self._metadata.get(name, default)


@implementer(IGlobalMediaSettings)
class GlobalSettings(Base):
    use_interface = IGlobalMediaSettings
