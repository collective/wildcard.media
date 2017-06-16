from plone.dexterity.browser import edit
from z3c.form.interfaces import DISPLAY_MODE


class VideoEditForm(edit.DefaultEditForm):

    @property
    def description(self):
        return "Edit video"

    def updateWidgets(self):
        super(VideoEditForm, self).updateWidgets()
        # IF uploaded to youtube
        #   hide video_file, upload to youtube, read only youtube url
        if getattr(self.context, 'upload_video_to_youtube', False):
            self.widgets['IVideo.video_file'].mode = DISPLAY_MODE
            self.widgets['IVideo.video_url'].mode = DISPLAY_MODE