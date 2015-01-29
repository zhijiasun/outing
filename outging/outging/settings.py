#coding:utf-8
"""
Django settings for outging project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import logging
import django.utils.log
import logging.handlers
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, "../static").replace('\\', '/')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'iejzv!wodu^ui)!@hp3s*goyxk(8x=hg3fpzl-z@@4ue)9s2w='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'xadmin',
    'crispy_forms',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'outging.urls'

WSGI_APPLICATION = 'outging.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
LOGIN_URL = '/login'
LOGGING = {
   'version': 1,
   'disable_existing_loggers': True,
   'formatters': {
       'standard': {
           'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}  #定义日志格式，供后面handler的定义使用，可以定义多个。 
       },
   'filters': {
       },
   'handlers': {#
       'mail_admins': {
           'level': 'ERROR',
           'class': 'django.utils.log.AdminEmailHandler',
           'include_html': True,
           },
       'default': {
           'level':'DEBUG',
           'class':'logging.handlers.RotatingFileHandler',
           # 'filename': '/sourceDns/log/all.log',     #日志输出文件
           'filename': BASE_DIR + 'all.log',     #日志输出文件
           'maxBytes': 1024*1024*5,                  #文件大小 
           'backupCount': 5,                         #备份份数
           'formatter':'standard',                   #使用哪种formatters日志格式
           },
       'error': {
           'level':'ERROR',
           'class':'logging.handlers.RotatingFileHandler',
           'filename': BASE_DIR + 'error.log',
           'maxBytes':1024*1024*5,
           'backupCount': 5,
           'formatter':'standard',
           },
       'main_debug': {
           'level':'DEBUG',
           'class':'logging.handlers.RotatingFileHandler',
           'filename': os.path.join(BASE_DIR, 'logs/main_debug.log'),
           'maxBytes':1024*1024*5,
           'backupCount': 5,
           'formatter':'standard',
           },
       'console':{
           'level': 'DEBUG',
           'class': 'logging.StreamHandler',
           'formatter': 'standard'
           },
       'request_handler': {
           'level':'DEBUG',
           'class':'logging.handlers.RotatingFileHandler',
           'filename': BASE_DIR + 'script.log', 
           'maxBytes': 1024*1024*5, 
           'backupCount': 5,
           'formatter':'standard',
           },
       'scprits_handler': {
           'level':'DEBUG',
           'class':'logging.handlers.RotatingFileHandler',
           'filename':BASE_DIR + 'script.log', 
           'maxBytes': 1024*1024*5, 
           'backupCount': 5,
           'formatter':'standard',
           }
       },
   'loggers': {
           'django': {
               'handlers': ['default'],
               'level': 'DEBUG',
               'propagate': False 
               },
           'django.request': {
               'handlers': ['request_handler'],
               'level': 'DEBUG',
               'propagate': False,
               },
           # 'scripts': { 
           #     'handlers': ['scprits_handler'],
           #     'level': 'INFO',
           #     'propagate': False
           #     },
           # 'sourceDns.webdns.views': {
           #     'handlers': ['default', 'error'],
           #     'level': 'DEBUG',
           #     'propagate': True
           #     },
           'main': {
               'handlers': ['console', 'main_debug'],
               'level': 'DEBUG',
               'propagate': True
               }
           }
   }
