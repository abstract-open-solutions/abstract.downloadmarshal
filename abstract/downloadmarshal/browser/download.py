#-*- coding: utf-8 -*-

from zExceptions import Unauthorized

from zope.component import queryMultiAdapter

from plone.namedfile.browser import Download as BaseDownload

from ..interfaces import IMarshal


class Download(BaseDownload):

    def __call__(self):
        marshal = self.get_marshal()
        if marshal and marshal.validate():
            marshal.consume()
            return super(Download, self).__call__()
        raise Unauthorized('ennó! non puoi scaricare!')

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

