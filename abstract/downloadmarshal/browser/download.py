#-*- coding: utf-8 -*-

from zExceptions import Unauthorized

from zope.component import queryMultiAdapter

from plone.namedfile.browser import Download as BaseDownload

from ..interfaces import IMarshal


class Download(BaseDownload):

    def __call__(self):
        message = "you cannot download this!"
        marshal = self.get_marshal()
        if marshal:
            is_valid, message = marshal.validate()
            if is_valid:
                marshal.consume()
                return super(Download, self).__call__()
        url = self.context.absolute_url()
        self.request.response.redirect(url)
        # raise Unauthorized(message)

    def get_marshal(self):
        marshal = None
        if self.fieldname:
            marshal = queryMultiAdapter((self.context, self.request),
                                          IMarshal,
                                          name=self.fieldname)

        if marshal is None:
            marshal = queryMultiAdapter((self.context, self.request),
                                          IMarshal)
        return marshal

