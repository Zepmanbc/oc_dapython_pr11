from . import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://4cc8d88b64444388a3fbbc92cf017305@sentry.io/1445027",
    integrations=[DjangoIntegration()]
)

DEBUG = False
ALLOWED_HOSTS = ['18.222.24.163']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

MIDDLEWARE.remove('whitenoise.middleware.WhiteNoiseMiddleware')
