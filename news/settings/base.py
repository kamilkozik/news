
from os.path import dirname, abspath, join
from .celery_base import *


BASE_DIR = dirname(dirname(dirname(abspath(__file__))))

# TODO: implement some clever way for hiding secret key
SECRET_KEY = '9c=o+i!2q4912m9ycpw2&!mzw6y#f-q&df)ty2z#66uj=!cp^='
SOCIAL_AUTH_FACEBOOK_KEY = open(join(dirname(dirname(BASE_DIR)), 'dev/secret/key')).read()
SOCIAL_AUTH_FACEBOOK_SECRET = open(join(dirname(dirname(BASE_DIR)), 'dev/secret/secret')).read()
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/news/'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'locale': 'pl_pl',
    'fields': 'id, name, email, age_range',
}


DEBUG = True
ALLOWED_HOSTS = [
    'localhost:8000'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',

    # news apps
    'news.apps.news',
    'news.apps.person',
    'news.apps.common',

    # social authentication
    'social.apps.django_app.default',

    'sorl.thumbnail',
    'sortedm2m'

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware'
]

ROOT_URLCONF = 'news.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'news.context_processors.base',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect'
            ],
        },
    },
]

WSGI_APPLICATION = 'news.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

LANGUAGE_CODE = 'pl'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'public', 'static')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
]

# Users Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR, 'private', 'media')

STATICFILES_DIRS = [
    MEDIA_ROOT
]

# DJANGO_PRECOMPILERS settings
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}',),
)
COMPRESS_OUTPUT_DIR = 'compressed'
COMPRESS_ENABLED = False

# AUTH settings
LOGIN_URL = '/auth/log/'

if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    INSTALLED_APPS += [
        'debug_toolbar'
    ]

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'kamil.kozik.kzq@gmail.com'
EMAIL_HOST_PASSWORD = open(join(dirname(dirname(BASE_DIR)), 'dev/secret/google')).read()
