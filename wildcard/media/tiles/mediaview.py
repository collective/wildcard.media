from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone.app.uuid.utils import uuidToObject
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implements

from wildcard.media import _


class IMediaViewTile(IPersistentCoverTile):
    title = schema.TextLine(
        title=_(u'Title'),
        required=False
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False
    )

    uuid = schema.TextLine(
        title=_(u'UUID'),
        required=False,
        readonly=True
    )


class MediaViewTile(PersistentCoverTile):
    implements(IMediaViewTile)

    index = ViewPageTemplateFile('templates/mediaview.pt')

    is_configurable = True
    is_editable = True
    is_droppable = True
    short_name = _('msg_short_name_mediaview', default=u'Media View')

    def is_empty(self):
        return self.data.get('uuid', None) is None

    def populate_with_object(self, obj):
        super(MediaViewTile, self).populate_with_object(obj)

        if obj.portal_type not in self.accepted_ct():
            return

        title = safe_unicode(obj.Title())
        desc = safe_unicode(obj.Description())
        uuid = IUUID(obj)
        media_height = getattr(obj, "height", "")
        media_width = getattr(obj, "width", "")

        data_mgr = ITileDataManager(self)
        data_mgr.set({
            'title': title,
            'description': desc,
            'uuid': uuid,
            'media_height': media_height,
            'media_width': media_width
        })

    def accepted_ct(self):
        return ['WildcardVideo','WildcardAudio']

    def media_absolute_url(self):
        uuid = self.data.get('uuid', None)
        if not uuid:
            return ''
        obj = uuidToObject(uuid)
        return obj.absolute_url()

    def media_context(self):
        uuid = self.data.get('uuid', None)
        if not uuid:
            return ''
        obj = uuidToObject(uuid)
        return obj

    def is_video(self):
        uuid = self.data.get('uuid', None)
        if not uuid:
            return ''
        obj = uuidToObject(uuid)
        return obj.portal_type == "WildcardVideo"

