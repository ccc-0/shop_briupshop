from django.urls import path,re_path
from django.conf.urls import url
from .views import *

app_name = '[goods]'  #反向解析

urlpatterns = [
    # path(r"index/",index,name='index'),
    path(r"index/",IndexView.as_view(),name='index'),
    # path(r'detail/',GoodsDetail.as_view(),name='detail'),
    # url(r'detail/([0-9]+)/',GoodsDetail.as_view(),name='detail'), #url传参
    # re_path(r'detail/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})',GoodsDetail.as_view(),name='detail'),
    path(r'detail/<int:id>/',GoodsDetail.as_view(),name='detail'),
    path(r"list/<int:id>/",GoodsList.as_view(),name='list'),

]
