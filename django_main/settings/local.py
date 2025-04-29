__author__ = '@SCTongYe'

from .base import *

ALLOWED_HOSTS = ['*']

DEBUG = True

# 老数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, "db.sqlite3"),
    },

}



STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

