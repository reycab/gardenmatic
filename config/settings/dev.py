from .base import *  # noqa

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    '*',
)

INSTALLED_APPS = INSTALLED_APPS + [  # noqa
    'django_extensions',
]
