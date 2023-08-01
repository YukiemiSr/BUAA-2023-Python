# -*- coding = utf-8 -*-
# @Time : 2023-07-22 15:13
# @Author : mfk
# @File : middleware.py
# @Software : PyCharm
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

# 中间件，用于用户认证
class sessionCheck(MiddlewareMixin):
    def process_request(self, request):
        # 排除那些不需要登录就能够访问的页面
        if request.path_info == "/login/" or request.path_info == "/register/" or request.path_info == '/test/':
            return
        # 读取当前访问用户的resssion信息
        info = request.session.get("info")
        if info:
            return
        # 没有登录过则要返回显示登录页面
        return redirect("/login/")

    def process_response(self, request, response):
        return response
