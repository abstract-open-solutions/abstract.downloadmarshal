import sys
import random

from zope.component import getUtility

from plone.registry.interfaces import IRegistry

from interfaces import IMarshalGlobalSettings


TOKEN_REQUEST_VAR = 'download-token'


def _generate_token():
    return random.randint(1, sys.maxint)


def get_settings():
    return getUtility(IRegistry).forInterface(IMarshalGlobalSettings, False)
