# @Time: 2022/9/6 23:50
# @Author: DoubleApple
from home.views import IndexView
from home.views import DetailView
from django.urls import path

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('detail/', DetailView.as_view(), name='detail')
]
