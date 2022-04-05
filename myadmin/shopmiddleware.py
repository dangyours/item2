from django.shortcuts import redirect
from django.urls import reverse

import re

class ShopMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        print("ShopMiddleware")

    def __call__(self, request):

        # 获取当前请求路径
        path = request.path

        ulist = ['/myadmin/login','/myadmin/logout','/myadmin/dologin']
        if re.match(r"^/myadmin",path) and (path not in ulist):
            if "adminuser" not in request.session:
                return redirect(reverse("myadmin_login"))


        # 请求继续执行下去
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response