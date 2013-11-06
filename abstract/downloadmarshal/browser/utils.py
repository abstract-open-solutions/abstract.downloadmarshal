#-*- coding: utf-8 -*-
from zope.component import queryMultiAdapter
from ..interfaces import IMarshal


class MarshalViewMixIn(object):

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
