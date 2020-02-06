import six.moves.urllib.request, six.moves.urllib.parse, six.moves.urllib.error

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as pmf
from Products.Five import BrowserView
from plone import api
from plone.z3cform.layout import wrap_form
from plone.memoize.instance import memoize
from wildcard.media import _
from wildcard.media.behavior import IVideo
from wildcard.media.config import getFormat
from wildcard.media.interfaces import IGlobalMediaSettings
from wildcard.media.interfaces import IMediaEnabled
from wildcard.media.settings import GlobalSettings
from wildcard.media.subscribers import video_edited
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form import group
from zope.component.hooks import getSite
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

class VideoView(BrowserView):

    def get_embed_url(self):
        """
        Try to guess video id from a various case of possible youtube urls and
        returns the correct url for embed.
        For example:
        - 'https://youtu.be/VIDEO_ID'
        - 'https://www.youtube.com/watch?v=VIDEO_ID'
        - 'https://www.youtube.com/embed/2Lb2BiUC898'
        """
        video_behavior = IVideo(self.context)
        if not video_behavior:
            return ""
        video_id = video_behavior.get_youtube_id_from_url()
        if not video_id:
            return ""
        return "https://www.youtube.com/embed/" + video_id

    def get_edit_url(self):
        """
        If the user can edit the video, returns the edit url.
        """
        if not api.user.has_permission(
            'Modify portal content',
            obj=self.context):
            return ""
        from plone.protect.utils import addTokenToUrl
        url = "%s/@@edit" % self.context.absolute_url()
        return addTokenToUrl(url)

class DefaultGroup(group.Group):
    label = u"Default"
    fields = field.Fields(IGlobalMediaSettings).select(
        "additional_video_formats", "async_quota_size",
        "default_video_width", "default_video_height")

class ConversionSettingsGroup(group.Group):
    label = u"Conversion settings"
    fields = field.Fields(IGlobalMediaSettings).select(
        "force", "avconv_in_mp4", "avconv_out_mp4",
        "avconv_in_webm", "avconv_out_webm",
        "avconv_in_ogg", "avconv_out_ogg")

class GlobalSettingsForm(group.GroupForm, form.EditForm):
    groups = (DefaultGroup, ConversionSettingsGroup)

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
        # Mark the video as not converted
        self.context.video_converted = False
        video_edited(self.context, None)
        self.request.response.redirect(self.context.absolute_url())


class Utils(MediaView):

    def valid_type(self):
        return IMediaEnabled.providedBy(self.context)

    @memoize
    def settings(self):
        return GlobalSettings(getSite())

    @property
    @memoize
    def base_wurl(self):
        base_url = self.context.absolute_url()
        return base_url + '/@@view/++widget++form.widgets.'

    @property
    @memoize
    def base_furl(self):
        return self.base_wurl + 'IVideo.'

    @memoize
    def videos(self):
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
                    'url': self.base_furl + fieldname + '/@@stream'
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
            return six.moves.urllib.parse.quote_plus(url)
        else:
            return url

    @memoize
    def image_url_quoted(self):
        url = self.image_url()
        if url:
            return six.moves.urllib.parse.quote_plus(url)
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
