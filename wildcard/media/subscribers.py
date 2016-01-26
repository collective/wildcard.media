import requests

from plone.namedfile.file import NamedBlobImage
from requests.exceptions import Timeout

from wildcard.media import logger
from wildcard.media.async import (
    convertVideoFormats,
    uploadToYouTube,
    removeFromYouTube,
    updateYouTubePermissions,
    editYouTubeVideo)
from wildcard.media.behavior import IVideo


def video_added(video, event):
    if getattr(video, 'video_file', None):
        if getattr(video, 'upload_video_to_youtube', False):
            uploadToYouTube(video)
            retrieveThumbFromYoutube(video)
        else:
            convertVideoFormats(video)
    if getattr(video, 'youtube_url', None):
        retrieveThumbFromYoutube(video)


def video_edited(video, event):
    if getattr(video, 'youtube_url', None):
        retrieveThumbFromYoutube(video)
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


def retrieveThumbFromYoutube(video):
    """
    Try to call Youtube service to retrieve video thumbnail
    and save it in the video
    """
    video_behavior = IVideo(video)
    if not video_behavior:
        return
    video_id = video_behavior.get_youtube_id_from_url()
    if not video_id:
        return
    url = "http://img.youtube.com/vi/%s/0.jpg" % video_id
    try:
        res = requests.get(url, stream=True, timeout=10)
    except Timeout:
        logger.error('Unable to retrieve thumbnail image for "%s": timeout.' % video_id)
        return
    except Exception as e:
        logger.error('Unable to retrieve thumbnail from "%s".' % url)
        logger.exception(e)
        return
    if not res.ok:
        if res.status_code == 404:
            logger.error('Unable to retrieve thumbnail from "%s". Not found.' % url)
        else:
            logger.error('Unable to retrieve thumbnail from "%s". Error: %s' % (url, res.status_code))
        return None
    video.image = NamedBlobImage(res.raw.data, filename=u'%s.jpg' % video_id)
