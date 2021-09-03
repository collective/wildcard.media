from ZODB.POSException import POSKeyError
from collective.celery import task
from wildcard.media import convert
try:
    from wildcard.media import youtube
except ImportError:
    youtube = None

import time


@task.as_admin(autoretry_for=(POSKeyError,), retry_backoff=5,
               name='wildcard.media.convertVideoFormats')
def convertVideoFormats(context):
    convert.convertVideoFormats(context)


@task.as_admin(name='wildcard.media.uploadToYouTube')
def uploadToYouTube(context):
    youtube.uploadToYouTube(context)


@task.as_admin(name='wildcard.media.removeFromYouTube')
def removeFromYouTube(context):
    youtube.removeFromYouTube(context)


@task.as_admin(name='wildcard.media.updateYouTubePermissions')
def updateYouTubePermissions(context):
    youtube.updateYouTubePermissions(context)


@task.as_admin(name='wildcard.media.editYouTubeVideo')
def editYouTubeVideo(context):
    youtube.editYouTubeVideo(context)
