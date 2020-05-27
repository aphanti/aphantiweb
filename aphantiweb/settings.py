"""
Django settings for aphantiweb project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import json 


WEB_INFO_JSON = '/opt/aphanti/web_info.json'
web_info = json.load(open(WEB_INFO_JSON, 'r'))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = web_info['APHANTI_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
if web_info['APHANTI_ENV'] == 'dev':
    DEBUG = True
else:
    DEBUG = False 
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_SSL_REDIRECT = True
    X_FRAME_OPTIONS = 'DENY'    


ALLOWED_HOSTS = ['*', '142.93.196.25', 'localhost', '127.0.0.1', 'aphanti.com', 'www.aphanti.com']

AUTH_USER_MODEL = 'accounts.WebUser'

#-------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = web_info['EMAIL_HOST_USER']
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = web_info['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
#-------------------------------------------------

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'django.contrib.sites', # social account
    'allauth', # social account
    'allauth.account', # social account
    'allauth.socialaccount',  # social account
    'allauth.socialaccount.providers.google', # social account
    'allauth.socialaccount.providers.facebook', # social account
    'allauth.socialaccount.providers.instagram', # social account
    'allauth.socialaccount.providers.twitter', # social account
    'accounts', 
    'home', 
    'blog', 
    'widget_tweaks', 
    'ckeditor', 
    'ckeditor_uploader', 
    'django_user_agents', 
    'tracking_analyzer', 
    'django_social_share', 
    #'django_user_agents', 
]

GEOIP_PATH = web_info['GEOIP_PATH']

# Cache backend is optional, but recommended to speed up user agent parsing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'


MIDDLEWARE = [
#MIDDLEWARE_CLASSES = [ 
    'django.middleware.security.SecurityMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 
    'django_user_agents.middleware.UserAgentMiddleware',
]


ROOT_URLCONF = 'aphantiweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ 
            os.path.join(BASE_DIR, 'templates'), 
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'aphantiweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': web_info['APHANTI_MYSQL_DBNAME'],
        'USER': web_info['APHANTI_MYSQL_USER'],
        'PASSWORD': web_info['APHANTI_MYSQL_PASSWORD'],
        'HOST': 'localhost',
        'PORT': 3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
# The absolute path to the directory where collectstatic will collect static files for deployment.
# The URL to use when referring to static files (where they will be served from)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'


# Static file serving.
# http://whitenoise.evans.io/en/stable/django.html#django-middleware
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


#=================================================================================
# social media account login

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', 
    'allauth.account.auth_backends.AuthenticationBackend', 
    )
SITE_ID = 1
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }, 
        'APP': {
            'client_id': web_info['google_app_client_id'], 
            'secret': web_info['google_app_client_secret'], 
            'key': web_info['google_app_client_secret'], 
        }
    }
}
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True

LOGIN_REDIRECT_URL = '/'

#=================================================================================


####################################
    ##  CKEDITOR CONFIGURATION ##
####################################

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = '/'
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = { 
    'comment': {
        'skin': 'moono', 
        'toolbar_Custom': [ 
            ['Format', 'Font', 'FontSize', '-', 'TextColor', 'BGColor'], 
            ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript'], 
            ['NumberedList', 'BulletedList', '-', 'Blockquote', '-', 'CodeSnippet', 'Mathjax'], 
        ], 
        'scayt_autoStartup': True, 
        'toolbar': 'Custom', 
        'height': 200, 
        'width': "100%", 
        'mathJaxLib': '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([ 
            'div', 
            'autolink', 
            'autoembed', 
            'embedsemantic', 
            'autogrow', 
            'widget', 
            'lineutils', 
            'clipboard', 
            'dialog', 
            'dialogui', 
            'elementspath', 
            'codesnippet', 
            'mathjax', 
            'scayt', 
        ]), 
    }, 
    'feedback': {
        'skin': 'moono', 
        'toolbar_Custom': [ 
            ['Format', 'Font', 'FontSize', '-', 'TextColor', 'BGColor'], 
            ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript'], 
            ['NumberedList', 'BulletedList'], 
        ], 
        'scayt_autoStartup': True, 
        'toolbar': 'Custom', 
        'height': 200, 
        'width': "100%", 
        'tabSpaces': 4,
        'extraPlugins': ','.join([ 
            'div', 
            'autolink', 
            'autoembed', 
            'embedsemantic', 
            'autogrow', 
            'widget', 
            'lineutils', 
            'clipboard', 
            'dialog', 
            'dialogui', 
            'elementspath', 
            'scayt', 
        ]), 
    }, 
    'default': {
        'skin': 'moono',
        #'skin': 'office2013',
        'toolbar_Basic': [
            [ 'Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': [
                #'Source', '-', 
                'Save', 'NewPage',
                #'Preview', 
                'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            #{'name': 'forms',
            # 'items': [#'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 
            #            'ImageButton',
            #            #'HiddenField', 
            #            ]},
            {'name': 'insert',
             'items': ['Link', 'Unlink', '-', 'Image',
                 #'Flash', 
                 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak',
                 #'Iframe', 
                 '-', 'CodeSnippet', 'Mathjax', 
                 ]},
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',
            ]},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript',
                 #'-', 'RemoveFormat'
                 ]},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote',
                        #'CreateDiv', 
                        '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
                       #'-', 'BidiLtr', 'BidiRtl','Language', 
                       ]},
             #{'name': 'links', 'items': ['Link', 'Unlink', 
             #    #'Anchor', 
             #   ]},
            {'name': 'styles', 'items': [
                #'Styles', 
                'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']}, 
            #{'name': 'tools', 'items': ['Maximize', 
            #    #'ShowBlocks', 
            #    ]},
            #{'name': 'about', 'items': ['About']},
            #'/',  # put this to force next toolbar on new line
        ], 
        'scayt_autoStartup': True, 
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        'height': 200,
        'width': "100%",
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        'mathJaxLib': '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            #'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath', 
            'codesnippet', 
            'mathjax', 
            'scayt', 
        ]),
    }
}
