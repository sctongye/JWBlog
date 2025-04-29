# -*- coding: utf-8 -*-
"""
Created by @南卡统爷 on 2019-08-26 3:21 PM.
"""
__author__ = '@SCTongYe'


from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api import models

class WJYAuth(BaseAuthentication):

    def authenticate(self, request):
        token = request.query_params.get('token')
        obj = models.UserToken.objects.filter(token=token).first()
        if not obj:
            raise AuthenticationFailed({'code':1001, 'error':'认证失败'})

        return (obj.user.user, obj)