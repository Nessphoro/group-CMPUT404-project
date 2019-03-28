"""
Django settings for socialproj project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import socket
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9gpl1u=h(+ise&p!a&3l=s88kv*cl9+-=-jfg0hkzpv27jevr='

if "PRODUCTION" in os.environ:
    DEBUG = True
    ALLOWED_HOSTS = [socket.getfqdn(), "localhost", "127.0.0.1"]
    print("Starting in prod")
    if "test" in socket.getfqdn():
        SOCIAL_AUTH_GITHUB_KEY = 'd4ab4da497a74368e983'
        SOCIAL_AUTH_GITHUB_SECRET = '04688004c72c9ee0c4ff75e1ec0772be6e3b00ea'
    else:
        SOCIAL_AUTH_GITHUB_KEY = '34f3467ad4c26f25b53c'
        SOCIAL_AUTH_GITHUB_SECRET = 'ff406247b5aedcfe59acecee32b7975179a0add1'
    SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SITE_URL = f"https://{socket.getfqdn()}"
    AUTHORS_DEFAULT_VERIFICATION = True # Controls if authors are verified by default
    LIMIT_NODE_TO_NODE_CONNECTIONS = False # Controls if the API requires HTTP Basic Auth
else:
    DEBUG = True
    ALLOWED_HOSTS = ["127.0.0.1",'testserver'] # testserver is for the testPost.py
    SOCIAL_AUTH_GITHUB_KEY = 'c55573c7ae415c79085c'
    SOCIAL_AUTH_GITHUB_SECRET = 'e03982182807e00ad9b3c469865b1635b9a85c4d'
    SITE_URL = "http://127.0.0.1:8000"
    AUTHORS_DEFAULT_VERIFICATION = True
    LIMIT_NODE_TO_NODE_CONNECTIONS = False


# SECURITY WARNING: don't run with debug turned on in production!
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']
LOGIN_REDIRECT_URL = '/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_jinja.contrib._humanize',
    'django.contrib.staticfiles',
    'django_jinja',
    'rest_framework',
    'socialapp.apps.SocialappConfig',
    'social_django',  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'socialproj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'NAME': 'jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            "match_extension": ".html",
            "app_dirname": "jinja2",
            'environment': 'socialapp.jinja2.environment',
            "filters": {
                "addclass": "socialapp.templatetags.addclass.addclass",
                "markdown": "socialapp.templatetags.markdown.md"
            },
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends', 
                'social_django.context_processors.login_redirect',            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends', 
                'social_django.context_processors.login_redirect', 
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
WSGI_APPLICATION = 'socialproj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if "PRODUCTION" in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/external/db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'static'),
)


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'socialapp.pipeline.save_profile',  
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

REST_FRAMEWORK = {
    "DATETIME_FORMAT": 'iso-8601',
 'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
}