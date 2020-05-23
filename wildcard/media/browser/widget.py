from Acquisition import aq_inner
from plone.formwidget.namedfile.interfaces import INamedFileWidget
from plone.formwidget.namedfile.widget import NamedFileWidget
from plone.namedfile.browser import Download
from plone.namedfile.interfaces import INamedFileField
from plone.namedfile.utils import stream_data
from z3c.form.interfaces import IFieldWidget, IFormLayer, IDataManager
from z3c.form.widget import FieldWidget
from zope.component import adapter, getMultiAdapter
from zope.interface import implementer, implementer_only
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
        """
        if self.context.ignoreContext:
            raise NotFound("Cannot get the data file from a widget with no context")

        if self.context.form is not None:
            content = aq_inner(self.context.form.getContent())
        else:
            content = aq_inner(self.context.context)

        field = aq_inner(self.context.field)

        dm = getMultiAdapter((content, field,), IDataManager)
        file_ = dm.get()
        if file_ is None:
            raise NotFound(self, self.request)

        request_range = self.handle_request_range(file_)
        return stream_data(file_, **request_range)
