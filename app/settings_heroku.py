from .settings import *
import dj_database_url

DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# Simplified static file serving.
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

COMPRESS_PRECOMPILERS = (
    ('text/less', '/app/.heroku/vendor/node/lib/node_modules/less/bin/lessc {infile} {outfile}'),
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
