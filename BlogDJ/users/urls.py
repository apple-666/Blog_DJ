# @Time: 2022/8/15 22:56
# @Author: DoubleApple
from django.urls import path
from users.views import *



urlpatterns = [
    # 参数1：路由
    # 参数2：视图函数
    # 参数3：路由名，方便通过reverse来获取路由
    path('register/', RegisterView.as_view(), name='register'),
    path('imagecode/', ImageCodeView.as_view(), name='imagecode'),
    path('smscode/', SmsCodeView.as_view(), name='smscode'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forget_password/', ForgetPasswordView.as_view(), name='forget_password')
    path('user_center/', UserCenterView.as_view(), name='user_center')
]
