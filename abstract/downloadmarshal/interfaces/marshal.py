from zope.interface import Interface
from zope import schema

# TODO: translations
_ = lambda x: x


class IMarshal(Interface):
    """ adapter for downloadable object
    """


class IMarshalStorageManager(Interface):
    """ adapter for handling storage on downloadable object
    """


class IMarshalGlobalSettings(Interface):
    """ settings registry
    """

    max_download_count = schema.Int(
        title=_(u"Max download count"),
        # description=_('Max numnber of download per token'),
        default=-1,
    )

    validity_days = schema.Int(
        title=_(u"Token validity days"),
        # description=_('How many days (from token creation) the token will be valid?'),
        default=-1,
    )

    bypass_roles = schema.Set(
        title=_(u"Bypass roles"),
        # description=_(u"The roles that bypass download check."),
        required=True,
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.Roles"
        ),
        default=set(['Manager',])
    )
