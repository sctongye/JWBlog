# -*- coding: utf-8 -*-
"""
Created by @南卡统爷 on 2019-08-26 1:11 AM.
"""
__author__ = '@SCTongYe'


from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from api import models
from api.auth.auth import WJYAuth
import uuid


class AuthView(APIView):

    def post(self, request, *args, **kwargs):
        # print(request.data)
        '''
        登录认证
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        ret = {'code': 1000}
        user = request.data.get('user')
        pwd = request.data.get('pwd')
        proj = request.data.get('projectname')

        user = models.UserInfo.objects.filter(
            user=user, pwd=pwd, proj=proj).first()
        if not user:
            ret['code'] = 1001
            ret['error'] = "Invalid Username or Password"
        else:
            uid = str(uuid.uuid4())
            models.UserToken.objects.update_or_create(
                user=user, defaults={'token': uid})
            ret['token'] = uid

        return Response(ret)


class MicroView(APIView):

    authentication_classes = [WJYAuth,]

    def get(self, request, *args, **kwargs):

        ret = {'code': 1000, 'title': '我弄阿帕奇欧美汇'}
        return Response(ret)
