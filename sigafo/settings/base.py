# Django settings for sigafo project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5$ak!f&amp;z619clp)x5^l#d(s($!!v6*dpfs)f%v@1)pgrln376x'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # default context processors for Django 1.4
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    # context processors for 'myproject'
    "sigafo.utils.context_processors.baseurl",
    "sigafo.utils.context_processors.sitetitle",
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sigafo.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'sigafo.wsgi.application'

import os.path
PROJECT_DIR = os.path.dirname(__file__) # this is not Django setting.

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, "..", "templates","default"),
    #os.path.join(PROJECT_DIR, "..", "templates","sb-admin-v2"),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # addons
    'django_hstore',
    'crispy_forms',
    'compressor',
    'leaflet',
    'djgeojson',
    'reversion',
    'django_extensions',
    'rest_framework',
    'bootstrap3',
    'haystack',
    'json_dbindex',
    'json_field',
    'django_aggtrigg',
    # project apps
    'sigafo.agrof',
    'sigafo.contact',
    'sigafo.parc',
    'sigafo.projet',
    'sigafo.map',
    'sigafo.referentiel',
    'sigafo.ressources',
    'sigafo.utils',
    'sigafo.osmboundary'
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (44.03, 3.59),
    'DEFAULT_ZOOM': 6,
    'MIN_ZOOM': 4,
    'MAX_ZOOM': 15,
    'RESET_VIEW': False,
    'PLUGINS': {
        'markercluster': {
            'css': ['/static/leaflet-plugins/vendor/MarkerCluster.css', 
                    '/static/leaflet-plugins/vendor/MarkerCluster.Default.css'],
            'js': '/static/leaflet-plugins/vendor/leaflet.markercluster.js',
            'auto-include': True,
            },
    }
    
}
#
#
# Compressor
#
COMPRESS_CSS_FILTERS = ['compressor.filters.csstidy.CSSTidyFilter']

COMPRESS_JS_FILTERS = ['compressor.filters.template.TemplateFilter']
# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'
#
#
#
LANGUAGES = (('en', 'English'),
             ('fr', 'French'))
