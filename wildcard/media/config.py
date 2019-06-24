ASYNC_DELAY = 30

class Format(object):

    def __init__(self, name, extension, type_):
        self.name = name
        self.extension = extension
        self.type_ = type_


CONVERTABLE_FORMATS = [
    Format('OGG', 'ogv', 'ogg'),
    Format('WebM', 'webm', 'webm')
]


def getFormat(type_):
    for tt in CONVERTABLE_FORMATS:
        if tt.type_ == type_:
            return tt


USE_ASYNC = True