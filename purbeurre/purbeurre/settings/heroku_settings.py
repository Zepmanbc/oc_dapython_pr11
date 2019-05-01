from . import *
import django_heroku

DEBUG = False
ALLOWED_HOSTS = ['bc-ocdapythonpr8.herokuapp.com']

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

django_heroku.settings(locals())