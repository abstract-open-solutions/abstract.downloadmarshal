#-*- coding: utf-8 -*-
from plone.namedfile.browser import Download as BaseDownload
from Products.statusmessages.interfaces import IStatusMessage

from .utils import MarshalViewMixIn
from .. import messageFactory as _


ERROR_MESSAGE = _(
    u"Sorry, you are not allowed to download "
    u"this resource.")


class Download(BaseDownload, MarshalViewMixIn):

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

    def set_headers(self, file):
        super(Download, self).set_headers(file)
        # we set some extra header to avoid caching
        self.request.response.addHeader('Pragma', "no-cache")
        self.request.response.addHeader('Cache-Control',
                                        'must-revalidate, \
                                        post-check=0, \
                                        pre-check=0, \
                                        public')
        self.request.response.addHeader('Expires', "0")

