# -*- coding: utf-8 -*-
"""
Created by @南卡统爷 on 2019-08-11 11:39 AM.
"""
__author__ = '@SCTongYe'


from .base import *


DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, "db.sqlite3")
    },

}


STATIC_ROOT = os.path.join(BASE_DIR, "static")
