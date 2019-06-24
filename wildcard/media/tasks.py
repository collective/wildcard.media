from ZODB.POSException import POSKeyError
from collective.celery import task
from wildcard.media import convert
try:
    from wildcard.media import youtube
except ImportError:
    youtube = None

import time


@task.as_admin(autoretry_for=(POSKeyError,), retry_backoff=5)
def convertVideoFormats(context):
    convert.convertVideoFormats(context)


@task.as_admin()
def uploadToYouTube(context):
    youtube.uploadToYouTube(context)


@task.as_admin()
def removeFromYouTube(context):
    youtube.removeFromYouTube(context)


@task.as_admin()
def updateYouTubePermissions(context):
    youtube.updateYouTubePermissions(context)


@task.as_admin()
def editYouTubeVideo(context):
    youtube.editYouTubeVideo(context)