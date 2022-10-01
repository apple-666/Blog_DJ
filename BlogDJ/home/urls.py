# @Time: 2022/9/6 23:50
# @Author: DoubleApple
from home.views import IndexView
from django.urls import path

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('detail/', IndexView.as_view(), name='detail')
]
