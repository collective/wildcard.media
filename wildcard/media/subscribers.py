# -*- coding: utf-8 -*-
from plone.namedfile.file import NamedBlobImage
from wildcard.media.async import (
    convertVideoFormats,
    uploadToYouTube,
    removeFromYouTube,
    updateYouTubePermissions,
    editYouTubeVideo)
from wildcard.media.behavior import IVideo
from wildcard.media.youtube import downloadThumbFromYouTube


def video_added(video, event):
    if getattr(video, 'video_file', None):
        if getattr(video, 'upload_video_to_youtube', False):
            uploadToYouTube(video)
        else:
            convertVideoFormats(video)
    elif getattr(video, 'youtube_url', None):
        retrieveThumbImage(video)


def video_edited(video, event):
    if getattr(video, 'youtube_url', None):
        retrieveThumbImage(video)
    elif getattr(video, 'youtube_data', False):
        if not getattr(video, 'upload_video_to_youtube', False):
            # previously set to put on youtube, but no longer set to be on youtube
            removeFromYouTube(video)
            convertVideoFormats(video)
        elif video.video_file and not getattr(video, 'video_converted', True):
            # new video set, need to upload
            uploadToYouTube(video)
        elif getattr(video, 'upload_video_to_youtube', False):
            editYouTubeVideo(video)
    else:
        if getattr(video, 'upload_video_to_youtube', False):
            # previously not on youtube, but now is, upload
            uploadToYouTube(video)
        elif video.video_file and not getattr(video, 'video_converted', True):
            convertVideoFormats(video)


def video_deleted(video, event):
    if getattr(video, 'upload_video_to_youtube', False):
        removeFromYouTube(video)


def video_state_changed(video, event):
    if (getattr(video, 'upload_video_to_youtube', False) and
            getattr(video, 'youtube_data', None)):
        # check permission
        updateYouTubePermissions(video)


def retrieveThumbImage(video):
    """
    Try to call YouTube service to retrieve video thumbnail
    and save it in the video
    """
    video_behavior = IVideo(video)
    if not video_behavior:
        return
    video_id = video_behavior.get_youtube_id_from_url()
    if not video_id:
        return
    image = downloadThumbFromYouTube(video_id)
    if not image:
        return
    video.image = NamedBlobImage(image, filename=u'%s.jpg' % video_id)
