from wildcard.media.async import (
    convertVideoFormats,
    uploadToYouTube,
    removeFromYouTube,
    updateYouTubePermissions,
    editYouTubeVideo)


def video_added(video, event):
    if video.video_file:
        if getattr(video, 'upload_video_to_youtube', False):
            uploadToYouTube(video)
        else:
            convertVideoFormats(video)


def video_edited(video, event):
    if getattr(video, 'youtube_data', False):
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