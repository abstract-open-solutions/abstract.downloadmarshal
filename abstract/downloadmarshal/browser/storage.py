#-*- coding: utf-8 -*-

from Products.Five.browser import BrowserView

from ..interfaces import IMarshalStorageManager


class View(BrowserView):
    """ a view for checking the content of the storage
    """

    def __call__(self):
        manager = IMarshalStorageManager(self.context)
        storage = manager.get_storage()
        lines = ["Download token storage", ]
        for token, data in storage.iteritems():
            lines.append("%s: %s" % (token, str(data)))
        return '\n'.join(lines)
