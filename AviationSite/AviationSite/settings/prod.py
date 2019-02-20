from .base import *
import os
import django_heroku
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY_AVSOC']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.avsoc.co.uk', '127.0.0.1', u'mmc21.host.cs.st-andrews.ac.uk','av-soc-website.herokuapp.com']

DEFAULT_FROM_EMAIL = 'aviation@st-andrews.ac.uk'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'Marlster7'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD_AVSOC']
EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DATABASES = {
    'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	# postgresql settings
	  	'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd4u0dhoqhidgu0',
        'USER': 'kflzeliaoljbzt',
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': 'ec2-54-83-17-151.compute-1.amazonaws.com',
        'PORT': '5432',
	}
}

# NOTE: set these to true once HTTPS is enabled (need SSL certificate)
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

CONN_MAX_AGE = 5

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# STATIC_ROOT = '/var/www/avsoc.co.uk/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_URL = '/static/'

django_heroku.settings(locals())
