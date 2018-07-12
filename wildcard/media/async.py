try:
    import collective.celery  # noqa
    from wildcard.media import tasks
except ImportError:
    tasks = None

from wildcard.media import pasync
from wildcard.media import convert
try:
    from wildcard.media import youtube
except ImportError:
    youtube = None
from wildcard.media.config import ASYNC_DELAY

from plone import api
from zope.globalrequest import getRequest


def _run(obj, func):
    if tasks:
        # collective.celery is installed
        tfunc = getattr(tasks, func.__name__)
        tfunc.apply_async(args=[obj], kwargs={}, countdown=ASYNC_DELAY)
    elif pasync.asyncInstalled():
        # plone.app.async installed
        pasync.queueJob(obj, func)
    else:
        func(obj)


def convertVideoFormats(video):
    api.portal.show_message(
        'Converting video to compatible formats. Be patient.',
        request=getRequest())
    _run(video, convert.convertVideoFormats)


def uploadToYouTube(video):
    if not youtube:
        return api.portal.show_message(
            'Whoops, trying to use YouTube but not configure correctly?',
            request=getRequest())
    api.portal.show_message(
        'Uploading video to YouTube. Check YouTube for status. '
        'Be patient while YouTube processes.',
        request=getRequest())
    _run(video, youtube.uploadToYouTube)


def removeFromYouTube(video):
    if not youtube:
        return api.portal.show_message(
            'Whoops, trying to use YouTube but not configure correctly?',
            request=getRequest())
    api.portal.show_message(
        'Removing video from YouTube. Be patient.',
        request=getRequest())
    _run(video, youtube.removeFromYouTube)


def updateYouTubePermissions(video):
    if not youtube:
        return api.portal.show_message(
            'Whoops, trying to use YouTube but not configure correctly?',
            request=getRequest())
    _run(video, youtube.updateYouTubePermissions)


def editYouTubeVideo(video):
    if not youtube:
        return api.portal.show_message(
            'Whoops, trying to use YouTube but not configure correctly?',
            request=getRequest())
    _run(video, youtube.editYouTubeVideo)
