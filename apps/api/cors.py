# -*- coding: utf-8 -*-
"""
Created by @南卡统爷 on 2019-08-22 2:31 PM.
"""
__author__ = '@SCTongYe'


from django.utils.deprecation import MiddlewareMixin


class CORSMiddleware(MiddlewareMixin):

    def process_response(self, request, response):

        # 添加响应头 允许你的域名来获取我的数据
        # response["Access-Control-Allow-Origin"] = '*'

        # 允许你携带 Content-Type 请求头 这里不能写 *
        # response["Access-Control-Allow-Headers"] = 'Content-Type'
        #
        # # 允许你发送 DELETE, PUT
        # response["Access-Control-Allow-Methods"] = 'DELETE, PUT' （HEAD GET POST 为简单请求标准之一所以无需添加）

        response["Access-Control-Allow-Origin"] = '*'

        if request.method == "OPTIONS":
            response["Access-Control-Allow-Headers"] = 'Content-Type'
            response["Access-Control-Allow-Methods"] = 'DELETE, PUT'

        return response