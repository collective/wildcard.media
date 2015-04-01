from plone import api
from wildcard.media.async import queueJob
from zope.globalrequest import getRequest


def video_added(video, event):
    if video.video_file:
        api.portal.show_message(
            'Converting video to compatible formats. Be patient.',
            request=getRequest())
        queueJob(video)


def video_edited(video, event):
    """ Convert if the video has been replaced """
    if video.video_file and not getattr(video, 'video_converted', True):
        api.portal.show_message(
            'Converting video to compatible formats. Be patient.',
            request=getRequest())
        queueJob(video)
