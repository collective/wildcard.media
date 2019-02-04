from zope.interface import implementer, implementer_only
from zope.component import adapter, getMultiAdapter
from z3c.form.interfaces import IFieldWidget, IFormLayer, IDataManager
from z3c.form.widget import FieldWidget
from plone.formwidget.namedfile.interfaces import INamedFileWidget
from plone.formwidget.namedfile.widget import NamedFileWidget, Download
from plone.namedfile.interfaces import INamedFileField
from plone.namedfile.utils import get_contenttype
# from plone.app.blob.field import BlobWrapper

from Acquisition import aq_inner
from zope.publisher.interfaces import NotFound


class IStreamNamedFileWidget(INamedFileWidget):
    pass


@implementer_only(IStreamNamedFileWidget)
class StreamNamedFileWidget(NamedFileWidget):
    pass


@implementer(IFieldWidget)
@adapter(INamedFileField, IFormLayer)
def StreamNamedFileFieldWidget(field, request):
    return FieldWidget(field, StreamNamedFileWidget(request))


class MediaStream(Download):
    """ Browser view for handling media streaming requests.
    """

    def __call__(self):
        """ Partially reproduced from plone.formwidget.namedfile.widget.Download.

        Leverages the existing BlobWrapper functionality to stream the media blobs
        to the client, allowing ranges and partial content.
        """
        if self.context.ignoreContext:
            raise NotFound("Cannot get the data file from a widget with no context")

        if self.context.form is not None:
            content = aq_inner(self.context.form.getContent())
        else:
            content = aq_inner(self.context.context)
        # from plone.dexterity.filerepresentation import DefaultReadFile
        # return DefaultReadFile(content)._getStream()

        field = aq_inner(self.context.field)

        dm = getMultiAdapter((content, field,), IDataManager)
        file_ = dm.get()
        if file_ is None:
            raise NotFound(self, self.request)
        # FIXME: BlobWrapper does not exists for py3
        # Find suitable replacement that works with dexterity.
        # sorry...
        return
        content_type = get_contenttype(file_)
        blob_wrapper = BlobWrapper(content_type)
        blob_wrapper.setBlob(file_)

        return blob_wrapper.index_html(self.request)
