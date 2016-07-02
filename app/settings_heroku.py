from .settings import *
import dj_database_url

DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# Simplified static file serving.
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

COMPRESS_PRECOMPILERS = (
    ('text/less', '/app/.heroku/vendor/node/lib/node_modules/less/bin/lessc {infile} {outfile}'),
)
