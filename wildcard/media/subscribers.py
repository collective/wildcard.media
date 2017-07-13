# -*- coding: utf-8 -*-
from plone import api
from plone.namedfile.file import NamedBlobImage
from wildcard.media.async import (
    convertVideoFormats,
    uploadToYouTube,
    removeFromYouTube,
    updateYouTubePermissions,
    editYouTubeVideo)
from wildcard.media import _
from wildcard.media.behavior import IVideo
from requests.exceptions import Timeout
from wildcard.media import logger
import requests


def video_added(video, event):
    if getattr(video, 'video_file', None):
        if getattr(video, 'upload_video_to_youtube', False):
            uploadToYouTube(video)
        else:
            convertVideoFormats(video)
    if getattr(video, 'video_url', None) and getattr(video, 'retrieve_thumb', False):
        # it has video_url set if is a remote video or is uploaded to youtube
        retrieveThumbImage(video)


def video_edited(video, event):
    if getattr(video, 'video_url', None) and getattr(video, 'retrieve_thumb', False):
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
    url = "https://i.ytimg.com/vi/%s/hqdefault.jpg" % video_id
    error_msg = _(
        'yt_image_download_error_label',
        'Unable to download thumbnail image automatically from youtube. Try later.'
    )
    try:
        res = requests.get(url, stream=True, timeout=10)
    except Timeout:
        logger.error(
            'Unable to retrieve thumbnail image for "%s": timeout.' % video_id)
        api.portal.show_message(
            message=error_msg,
            request=video.REQUEST,
            type="warning")
        return
    except Exception as e:
        logger.error('Unable to retrieve thumbnail from "%s".' % url)
        logger.exception(e)
        api.portal.show_message(
            message=error_msg,
            request=video.REQUEST,
            type="warning")
        return
    if not res.ok:
        if res.status_code == 404:
            logger.error(
                'Unable to retrieve thumbnail from "%s". Not found.' % url)
            error_msg = _(
                'yt_image_download_notfound_error_label',
                "Unable to download thumbnail image automatically from youtube. Probably it isn't available yet. Please retry in a few minutes."
            )
            api.portal.show_message(
                message=error_msg,
                request=video.REQUEST,
                type="warning")
        else:
            logger.error('Unable to retrieve thumbnail from "%s". Error: %s' % (url, res.status_code))
            api.portal.show_message(
                message=error_msg,
                request=video.REQUEST,
                type="warning")
        return
    video.image = NamedBlobImage(res.raw.data, filename=u'%s.jpg' % video_id)
    api.portal.show_message(
        message=_(
            'yt_image_download_success_label',
            'Thumbnail image correctly saved from youtube.'),
        request=video.REQUEST)
