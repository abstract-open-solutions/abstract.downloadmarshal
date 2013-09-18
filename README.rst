Introduction
============

A plone package for marshalling file downloads on Dexterity content types that have a file field.

Description
-----------

This package overrides `@@download` view for items marked with the interface `abstract.downloadmarshal.interfaces.IDownloadable`.
This view takes care of validating access to the file to be downloaded. ATM you need to activate it in your ZCML like this::

    <class class=".mycontent.Content">
        <implements interface="abstract.downloadmarshal.interfaces.IDownloadable" />
    </class>

TODO: make this a Dexterity behaviour.

Access to the resource is granted by a download token. The token is annotated onto the object and its use is restricted by the marshal settings.

Settings
--------

Settings are configurable via `plone.registry` with the interface `abstract.downloadmarshal.interfaces.IMarshalGlobalSettings`. From this record you can setup:

- max_download_count: max number of download per token (defaults to 1)
- validity_days: how many days the token will be usable since 1st download (defaults to -1, infinite)
- bypass_roles: a set of roles that can bypass the check (defaults to ['Manager',])


Marshal
-------

The marshal is an multi adapter implementing `abstract.downloadmarshal.interfaces.IMarshal` that takes a context (the downloadable resource) and a request. It takes care of validating the access to the resource via validators (see later) and to generate a token if needed and store into annotation via its storage manager (an adapter registered as `abstract.downloadmarshal.interfaces.IMarshalStorageManager`). Every registered token matches a `date` and a `count`, token creation date and download count respectively.

A marshal is registered by default and you can register validator against it. You can also register your own named adapter for a specific download field, for instance:

    <adapter factory=".adapters.Marshal" name="my_file_field" />

that will let you handle downloads of `path/to/resource/@@download/my_file_field` from your custom marshal. See `abstract.downloadmarshal.adapters.Marshal` to see how it's implemented.

Validators
----------

Validators are use to validate the access to the resource. A validator is simply a multi adapter implementing `abstract.downloadmarshal.interfaces.IValidator` and taking a marshal, a resource and a request. That means that you can customize validators per-marshal, per-resource and per-request.

Validators are called one by one and if only one of the validator do not validate positevely the request the validation will fail and the resource will not be downloadable.

The are two default validators right now: one that validates `max_download_count` and one that validates `validity_days`.
You are allowed to add more validators by registered a named adapter like:

<adapter
    factory=".adapters.MyValidator"
    name="my_validator"
    />

see `abstract.downloadmarshal.adapters.Validator` to see how it's implemented.
