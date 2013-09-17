#-*- coding: utf-8 -*-

import datetime
from BTrees.IOBTree import IOBTree
from persistent.dict import PersistentDict

from zope import component
from zope import interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.annotation.interfaces import IAnnotations

from interfaces import IDownloadable
from interfaces import IMarshal
from interfaces import IMarshalStorageManager
from utils import _generate_token
from utils import get_settings
from utils import TOKEN_REQUEST_VAR

ANN_KEY = 'abstract.downloadmarshal:storage'


class MarshalStorageManager(object):

    interface.implements(IMarshalStorageManager)
    component.adapts(IDownloadable)

    def __init__(self, context):
        self.context = context

    def get_storage(self):
        annotations = IAnnotations(self.context)
        if ANN_KEY not in annotations.keys():
            annotations[ANN_KEY] = IOBTree()
        return annotations[ANN_KEY]

    def has_key(self, key):
        storage = self.get_storage()
        return storage.has_key(key)

    def save(self, key, data, check=True):
        storage = self.get_storage()
        if check and self.has_key(key):
            raise ValueError("The key '%s' already exist!" % key)
        storage[key] = PersistentDict(data)

    def update(self, key):
        storage = self.get_storage()
        if storage.has_key(key):
            data = storage[key]
        else:
            data = {
                'date': datetime.date.today(),
                'count': 1,
            }
        data['count'] = data.get('count', 0) + 1
        self.save(key, data, check=False)


class Marshal(object):

    interface.implements(IMarshal)
    component.adapts(IDownloadable, IBrowserRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.storage_manager = IMarshalStorageManager(context)
        self.settings = get_settings()

    def generate_token(self, consume=False):
        storage = self.storage_manager.get_storage()
        token = _generate_token()
        while storage.has_key(token):
            token = _generate_token()
        if consume:
            self.consume(token)
        return token

    def consume(self, token):
        self.storage_manager.update(token)

    def request_has_token(self):
        return self.request.get(TOKEN_REQUEST_VAR)

    def can_bypass(self):
        can = False
        member = self.ps.member()
        member_roles = member.getRoles()
        for role in self.settings.bypass_roles:
            if role in member_roles:
                can = True
                break
        return can

    def validate(self, token=None):
        if token is None:
            token = self.request.get(TOKEN_REQUEST_VAR)
        if token is None and not self.can_bypass():
            return False
        storage = self.storage_manager.get_storage()
        if not storage.has_key(token):
            return False
        data = storage[token]
        count_check = True
        date_check = True
        # check download limit
        if self.settings.max_download_count > 0:
            count_check = False
            if data['count'] <= self.settings.max_download_count:
                count_check = True
        if self.settings.validity_days > 0:
            date_check = False
            delta = datetime.timedelta(self.settings.validity_days)
            max_date = data['date'] + delta
            today = datetime.date.today()
            if today <= max_date:
                date_check = True
        return count_check and date_check


