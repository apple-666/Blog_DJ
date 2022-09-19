# @Time: 2022/8/15 22:55
# @Author: DoubleApple
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest, HttpResponse
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import JsonResponse
from utils.response_code import RETCODE
from libs.yuntongxun.sms import CCP
from random import randint
from django.urls import reverse
from django.shortcuts import redirect
import re
from users.models import User
from django.db import DatabaseError
import logging
logger = logging.getLogger('django')



class RegisterView(View):
    """用户注册"""
    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        return render(request, 'register.html')

    def post(self, request):
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        smscode = request.POST.get('sms_code')
        # print("mobile:" + mobile)
        # print("password:" + password)
        # print("password2:" + password2)
        if not all([mobile, password, password2, smscode]):
            return HttpResponseBadRequest('缺少必要参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号码错误')
        if not re.match(r'^[0-9a-zA-Z]{1,20}$', password):
            return HttpResponseBadRequest('请输入>=1个数字或者大小写字母')
        if password != password2:
            return HttpResponseBadRequest('两次输入的密码不一致')

        redis_connection = get_redis_connection('default')
        sms_code_redis = redis_connection.get('sms:%s' % mobile)
        sms_code_redis = sms_code_redis.decode()  # code在网络中是bytes形式，要解码成str
        # print(sms_code_redis)
        # print(smscode)
        if sms_code_redis is None:
            return HttpResponseBadRequest('短信验证码已过期')
        if sms_code_redis != smscode:
            return HttpResponseBadRequest('短信验证码错误')

        try:
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)
        except DatabaseError:
            return HttpResponseBadRequest('注册失败')

        # from django.contrib.auth import login
        # 注册 ->  保存登录状态
        login(request, user)
        # namespace : name  来获取路由
        response = redirect(reverse('home:index'))
        response.set_cookie('is_login', True)
        response.set_cookie('username', user.username, max_age=30*24*3600)
        return response


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


class SmsCodeView(View):

    def get(self, request):
        mobile = request.GET.get('mobile')
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        if not all([mobile, image_code, uuid]):
            return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少参数'})
        redis_connection = get_redis_connection('default')
        image_code_redis = redis_connection.get('img:%s' % uuid)
        if image_code_redis is None:
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码失效'})
        try:
            redis_connection.delete('img:%s' % uuid)
        except Exception as e:
            logger.error(e)

        # print("image_code_redis:" + str(image_code_redis))
        logger.info(image_code_redis)
        image_code_redis = image_code_redis.decode() # 转str
        if image_code_redis.lower() != image_code.lower():
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码错误'})
        sms_code = "%06d" % randint(0, 999999)
        logger.info(sms_code)
        # print('sms 的码:' + sms_code)
        redis_connection.setex('sms:%s' % mobile, 1200, sms_code)
        CCP().send_template_sms(mobile, [sms_code, 30], 1)  # 30min
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '成功发送邮件'})


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 接受参数
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        # 校验参数
        # 判断参数是否齐全
        if not all([mobile, password]):
            return HttpResponseBadRequest('缺少必传参数')

        # 判断手机号是否正确
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('请输入正确的手机号')

        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{1,20}$', password):
            return HttpResponseBadRequest('密码最少1位，最长20位')

        # 认证登录用户
        # 认证字段已经在User模型中的USERNAME_FIELD = 'mobile'修改
        user = authenticate(mobile=mobile, password=password)

        if user is None:
            return HttpResponseBadRequest('用户名或密码错误')

        # 实现状态保持
        login(request, user)

        # 响应登录结果
        response = redirect(reverse('home:index'))

        # 设置状态保持的周期
        if remember != 'on':
            # 没有记住用户：浏览器会话结束就过期
            request.session.set_expiry(0)
            # 设置cookie
            response.set_cookie('is_login', True)
            response.set_cookie('username', user.username, max_age=30 * 24 * 3600)
        else:
            # 记住用户：None表示两周后过期
            request.session.set_expiry(None)
            # 设置cookie
            response.set_cookie('is_login', True, max_age=14 * 24 * 3600)
            response.set_cookie('username', user.username, max_age=30 * 24 * 3600)
        # 返回响应
        return response


from django.contrib.auth import logout


class LogoutView(View):
    def get(self, request):
        logout(request)
        response = redirect(reverse('home:index'))
        print(request.COOKIES.get('is_login'))

        response.delete_cookie('is_login')
        # response.delete_cookie('username')
        return response


