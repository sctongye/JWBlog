# -*- coding: utf-8 -*-
"""
Created by @南卡统爷 on 2019-08-29 12:56 PM.
"""
__author__ = '@SCTongYe'


import os


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'django_main.settings.local')
    # print(os.environ)

    import django
    django.setup()

    from frontend.models import UserInfo
    from django.contrib.auth.models import UserManager

    user = UserInfo.objects.get(username="tongye")
    # 如果没有 现在 frontend_userinfo 里创建一个新的 username

    from django.contrib.auth.hashers import make_password
    pwd = "xxxxx"
    hashed_pwd = make_password(pwd)
    user.password = hashed_pwd
    print("用户 '"+ str(user) +"' 的密码被更改为: ")
    print(hashed_pwd)
    user.save()
