#-*- coding: utf-8 -*-
from zope.component import queryMultiAdapter

from plone.namedfile.browser import Download as BaseDownload
from Products.statusmessages.interfaces import IStatusMessage

from ..interfaces import IMarshal
from .. import messageFactory as _


ERROR_MESSAGE = _(
    u"Sorry, you are not allowed to download "
    u"this resource.")


class Download(BaseDownload):

    def __call__(self):
        marshal = self.get_marshal()
        if marshal:
            is_valid, message = marshal.validate()
            if is_valid == 1:
                marshal.consume()
                return super(Download, self).__call__()
            elif is_valid == 2:
                return super(Download, self).__call__()

        IStatusMessage(self.request).addStatusMessage(
            ERROR_MESSAGE,
            type="error"
        )

        url = self.context.absolute_url()
        self.request.response.redirect(url)

    def get_marshal(self):
        marshal = None
        if self.fieldname:
            marshal = queryMultiAdapter(
                (self.context, self.request),
                IMarshal,
                name=self.fieldname
            )

        if marshal is None:
            marshal = queryMultiAdapter(
                (self.context, self.request),
                IMarshal
            )
        return marshal
