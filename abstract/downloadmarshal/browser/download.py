#-*- coding: utf-8 -*-

from zExceptions import Unauthorized

from zope.component import queryMultiAdapter

from plone.namedfile.browser import Download as BaseDownload

from ..interfaces import IMarshal


class Download(BaseDownload):

    def __call__(self):
        validator = self.get_validator()
        if validator and not validator.validate():
            raise Unauthorized('ennó! non puoi scaricare!')
        return super(Download, self).__call__()

    def get_validator(self):
        if self.fieldname:
            validator = queryMultiAdapter((self.context, self.request),
                                          IMarshal,
                                          name=self.fieldname)
        else:
            validator = queryMultiAdapter((self.context, self.request),
                                          IMarshal)
        return validator

