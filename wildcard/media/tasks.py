from ZODB.POSException import POSKeyError
from collective.celery import task
from wildcard.media import convert
try:
    from wildcard.media import youtube
except ImportError:
    youtube = None

import time


# XXX go back to using autoretry when retry is fixed in collective.celery
# @task.as_admin(autoretry_for=(POSKeyError,), retry_backoff=5)
@task.as_admin()
def convertVideoFormats(context):
    # XXX remove sleep when retry is fixed in collective.celery
    time.sleep(10)
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