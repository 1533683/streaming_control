"""
Django settings for notes project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7fbt!bl!3e^6ds@btdcw1aa+%b^0!yyllf9+rbpv3++-ahvq-*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'supervisord',
    'accounts',
    'log',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'setting.urls'

WSGI_APPLICATION = 'setting.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",    
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'streaming_control',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = (
BASE_DIR
)
MEDIA_URL = '/media/'

SUPERVISORD_CONFIG = '/etc/supervisord.d/'
EXTENTION = '.ini'
SUPERVIDORD_SERVICES= '/etc/init.d/supervisord'
SUPERVISORD_CONTROL= '/usr/bin/supervisorctl'

YOUTUBE_SERVER = 'rtmp://a.rtmp.youtube.com/live2/'
YOUTUBE_TEMPLATE = """[program:[name]]
command=ffmpeg -i udp://[source] -c:v copy -c:a copy -bsf:a aac_adtstoasc -f flv rtmp://a.rtmp.youtube.com/live2/[streamkey]
redirect_stderr=true
stdout_logfile= /var/log/supervisor/[name].log
#id: [streaming_id] owner: [owner_name] desc: [description]"""

FACEBOOK_SERVER = 'rtmp://rtmp-api.facebook.com:80/rtmp/'
FACEBOOK_TEMPLATE = """[program:[name]]
command=ffmpeg -i udp://[source] -vcodec copy -acodec aac -ab 192k -strict -2 -preset fast -f flv rtmp://rtmp-api.facebook.com:80/rtmp/[streamkey]
redirect stderr=true
stdout_logfile= /var/log/supervisor/[name].log
#id: [streaming_id] owner: [owner_name] desc: [description]"""
