from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from wildcard.media.interfaces import IGlobalMediaSettings
from z3c.form import form
from z3c.form import field
from z3c.form import button
from plone.app.z3cform.layout import wrap_form
from wildcard.media import _
from wildcard.media.settings import GlobalSettings
from wildcard.media.config import getFormat
from wildcard.media.async import queueJob
from wildcard.media.interfaces import IMediaEnabled


class MediaView(BrowserView):
    def setUp(self):
        context = self.context
        self.portal = getToolByName(context, 'portal_url').getPortalObject()
        portal_url = self.portal.absolute_url()
        self.base_url = context.absolute_url()
        self.base_wurl = self.base_url + '/@@view/++widget++form.widgets.'
        self.static = portal_url + '/++resource++wildcard-media'
        self.mstatic = self.static + '/mediaelementjs'


class AudioView(MediaView):
    def __call__(self):
        self.setUp()
        self.audio_url = '%sIAudio.audio_file/@@stream' % (
            self.base_wurl,
        )
        return self.index()


class VideoMacroView(MediaView):

    def __call__(self):
        context = self.context
        self.setUp()

        self.base_furl = self.base_wurl + 'IVideo.'
        types = [('mp4', 'video_file')]
        settings = GlobalSettings(self.portal)
        for type_ in settings.additional_video_formats:
            format = getFormat(type_)
            if format:
                types.append((format.type_,
                              'video_file_' + format.extension))
        self.videos = []
        for (_type, fieldname) in types:
            file = getattr(context, fieldname, None)
            if file:
                self.videos.append({
                    'type': _type,
                    'url': self.base_furl + fieldname + '/@@stream'
                })
        if self.videos:
            self.mp4_url = self.videos[0]['url']
        else:
            self.mp4_url = None
        image = getattr(self.context, 'image', None)
        if image:
            self.image_url = '%s/@@images/image' % (
                self.base_url
            )
        else:
            self.image_url = None
        subtitles = getattr(self.context, 'subtitle_file', None)
        if subtitles:
            self.subtitles_url = '%ssubtitle_file/@@download/%s' % (
                self.base_furl,
                subtitles.filename
            )
        else:
            self.subtitles_url = None

        self.width = getattr(context, 'width', 640)
        self.height = getattr(context, 'height', 320)
        return self.index()


class GlobalSettingsForm(form.EditForm):
    fields = field.Fields(IGlobalMediaSettings)

    label = _(u'heading_media_global_settings_form',
              default=u"Media Settings")
    description = _(u'description_media_global_settings_form',
                    default=u"Configure the parameters for media.")

    @button.buttonAndHandler(_('Save'), name='apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)

        self.status = _('Changes saved.')

GlobalSettingsFormView = wrap_form(GlobalSettingsForm)


class ConvertVideo(BrowserView):
    def __call__(self):
        queueJob(self.context)
        self.request.response.redirect(self.context.absolute_url())


class Utils(BrowserView):

    def valid_type(self):
        return IMediaEnabled.providedBy(self.context)
