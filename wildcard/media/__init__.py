from logging import getLogger
from zope.i18nmessageid import MessageFactory
from wildcard.media import permissions  # noqa
# permissions  # pyflakes

_ = MessageFactory('wildcard.media')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

logger = getLogger('wildcard.media')
