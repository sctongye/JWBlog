# -*- coding: utf-8 -*-
"""
Created by @南卡统爷 on 2019-08-21 1:56 PM.
"""
__author__ = '@SCTongYe'


from django.urls import path
from api.views import account

urlpatterns = [
    # re_path(r'^(?P<version>[v1|v2]+)/course/$', course.CourseView.as_view()),
    # 方法1：
    # path('course/', course.CourseView.as_view()),
    # re_path(r'^course/(?P<pk>\d+)$', course.CourseView.as_view()),


    path('auth/', account.AuthView.as_view()),
    path('micro/', account.MicroView.as_view()),

]
