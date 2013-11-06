#-*- coding: utf-8 -*-
from plone.namedfile.browser import DisplayFile as BaseView
from Products.statusmessages.interfaces import IStatusMessage

from .utils import MarshalViewMixIn
from .. import messageFactory as _


ERROR_MESSAGE = _(u"Sorry, you are not allowed to view this resource.")


class DisplayFile(BaseView, MarshalViewMixIn):

    def __call__(self):
        marshal = self.get_marshal()
        if marshal:
            is_valid, message = marshal.validate()
            if is_valid == 1:
                marshal.consume()
                return super(DisplayFile, self).__call__()
            elif is_valid == 2:
                return super(DisplayFile, self).__call__()

        IStatusMessage(self.request).addStatusMessage(
            ERROR_MESSAGE,
            type="error"
        )

        url = self.context.absolute_url()
        self.request.response.redirect(url)
