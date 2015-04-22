from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as pmf
from wildcard.media.interfaces import IGlobalMediaSettings
from z3c.form import form
from z3c.form import field
from z3c.form import button
from plone.app.z3cform.layout import wrap_form
from wildcard.media import _
from wildcard.media.settings import GlobalSettings
from wildcard.media.config import getFormat
from wildcard.media.interfaces import IMediaEnabled
from wildcard.media.subscribers import video_edited
import urllib
from plone.memoize.instance import memoize
from zope.interface import alsoProvides
try:
    from wildcard.media import youtube
except ImportError:
    youtube = False
try:
    from plone.protect.interfaces import IDisableCSRFProtection
except ImportError:
    from zope.interface import Interface as IDisableCSRFProtection  # noqa


class MediaView(BrowserView):

    @property
    @memoize
    def mstatic(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        portal_url = portal.absolute_url()
        static = portal_url + '/++resource++wildcard-media'
        return static + '/components/mediaelement/build'


class AudioView(MediaView):
    def __call__(self):
        base_url = self.context.absolute_url()
        base_wurl = base_url + '/@@view/++widget++form.widgets.'
        self.audio_url = '%sIAudio.audio_file/@@stream' % (
            base_wurl
        )
        self.ct = self.context.audio_file.contentType
        return self.index()


class GlobalSettingsForm(form.EditForm):
    fields = field.Fields(IGlobalMediaSettings)

    label = _(u"Media Settings")
    description = _(u'description_media_global_settings_form',
                    default=u"Configure the parameters for media.")

    @button.buttonAndHandler(pmf('Save'), name='apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)

        self.status = pmf('Changes saved.')

GlobalSettingsFormView = wrap_form(GlobalSettingsForm)


class ConvertVideo(BrowserView):
    def __call__(self):
        video_edited(self.context, None)
        self.request.response.redirect(self.context.absolute_url())


class Utils(MediaView):

    def valid_type(self):
        return IMediaEnabled.providedBy(self.context)

    @memoize
    def videos(self):
        base_url = self.context.absolute_url()
        base_wurl = base_url + '/@@view/++widget++form.widgets.'
        base_furl = base_wurl + 'IVideo.'
        types = [('mp4', 'video_file')]
        settings = GlobalSettings(
            getToolByName(self.context, 'portal_url').getPortalObject())
        for type_ in settings.additional_video_formats:
            format = getFormat(type_)
            if format:
                types.append((format.type_,
                              'video_file_' + format.extension))
        videos = []
        for (_type, fieldname) in types:
            file = getattr(self.context, fieldname, None)
            if file:
                videos.append({
                    'type': _type,
                    'url': base_furl + fieldname + '/@@stream'
                })
        return videos

    @memoize
    def mp4_url(self):
        videos = self.videos()
        if videos:
            return videos[0]['url']
        else:
            return None

    @memoize
    def subtitles_url(self):
        subtitles = getattr(self.context, 'subtitle_file', None)
        if subtitles:
            return '%ssubtitle_file/@@download/%s' % (
                self.base_furl,
                subtitles.filename
            )
        else:
            return None

    @memoize
    def image_url(self):
        image = getattr(self.context, 'image', None)
        if image:
            return '%s/@@images/image' % (
                self.context.absolute_url()
            )
        else:
            return None

    @memoize
    def mp4_url_quoted(self):
        url = self.mp4_url()
        if url:
            return urllib.quote_plus(url)
        else:
            return url

    @memoize
    def image_url_quoted(self):
        url = self.image_url()
        if url:
            return urllib.quote_plus(url)
        else:
            return url


class AuthorizeGoogle(BrowserView):

    def __call__(self):
        if not youtube:
            raise Exception("Error, dependencies for youtube support not present")
        if self.request.get('code'):
            alsoProvides(self.request, IDisableCSRFProtection)
            return youtube.GoogleAPI(self.request).confirm_authorization()
        else:
            return youtube.GoogleAPI(self.request).authorize()
