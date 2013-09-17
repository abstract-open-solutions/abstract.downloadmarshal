import sys
import random

from zope.component import getUtility

from plone.registry.interfaces import IRegistry

from interfaces import IMarshalGlobalSettings


TOKEN_REQUEST_VAR = 'download-token'

# max number allowd by IOBTree
MAX_NUMBER = 999999999

def _generate_token():
    return random.randint(1, MAX_NUMBER)


def get_settings():
    return getUtility(IRegistry).forInterface(IMarshalGlobalSettings, False)
