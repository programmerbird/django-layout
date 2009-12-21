#-*- coding:utf-8 -*-

# [debug]
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# [common] 
import os
INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.flatpages',
)
TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
	'django.core.context_processors.i18n',
	'django.core.context_processors.request',
	'django.core.context_processors.media',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'sdfs;dfkpoi23k4;.ds0p;fsdflsdfui1^4nfd1'

# [templates]
TEMPLATE_DIRS = (
	os.path.join(os.path.dirname(__file__), 'templates'),
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.doc.XViewMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
)

# [site]
import os  
ROOT_URLCONF = 'urls'
LOGIN_REDIRECT_URL = '/'
COMPANY_NAME = 'Extend Studio'
COMPANY_SLUG = 'extend'
COMPANY_STATE = 'Bangkok'
SITE_NAME = 'extend'
SITE_URL = 'http://www.x10studio.com/'

ADMINS = (
	('Sittipon Simasanti', 'sittipon@x10studio.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Asia/Bangkok'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/django/admin/'

PARSER_PLUGINS = (
	'hibird.parsers.vimeo.parse',
	'hibird.parsers.youtube.parse',
)

LANGUAGES = (
	('th', 'Thai'),
	('en', 'English'),
)
DEFAULT_LANGUAGE = 'en'
_=lambda (x) : x

# [database]
# On Linux, using mysql
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(os.path.dirname(__file__), 'db/layout.sqlite3')

# [registration]
INSTALLED_APPS += ('registration',)

# [hibird]
INSTALLED_APPS += ('hibird',)

# [current_user]
INSTALLED_APPS += ('current_user',)
MIDDLEWARE_CLASSES += (
	'current_user.middlewares.ThreadLocals',
)

# [page]
INSTALLED_APPS += ('page',)
PAGE_WIDGET_PATHS = (
	'page.widgets',
)
INSTALLED_APPS += ('publisher',)
PAGE_WIDGET_PATHS += (
	'publisher.widgets',
)

