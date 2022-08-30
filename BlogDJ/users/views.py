# @Time: 2022/8/15 22:55
# @Author: DoubleApple
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest,HttpResponse
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        return render(request, 'register.html')


class ImageCodeView(View):

    def get(self, request):
        uuid = request.GET.get('uuid')
        print(uuid)
        if uuid is None:
            return HttpResponseBadRequest('URL错误')
        text, image = captcha.generate_captcha()
        redis_connection = get_redis_connection('default')
        redis_connection.setex('img:%s' % uuid, 1200, text)  # s
        return HttpResponse(image, content_type='image/jpg')


