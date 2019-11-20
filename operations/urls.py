from django.urls import path,re_path
from django.conf.urls import url
from .views import *

app_name = '[operations]'  #反向解析

urlpatterns = [
    path(r"flow/",FlowListView.as_view(),name='flow'),#购物车页面
    path(r"flow2/",Flow2ListView.as_view(),name='flow2'),#购物车2页面
    path(r'add_flow/<int:good_id>/<int:nums>/',FlowAddView.as_view(),name='add_flow'), #添加入购物车
    path(r'deleteflow/',DeleteFlowView.as_view(),name='deleteflow'), #购物车的删除
    path(r'addorder/<str:goodids>/<str:goodnums>/<int:all_price>/',AddOrderView.as_view(),name='addorder'),#确认并去填写订单
    path(r'addaddress/',AddAddressView.as_view(),name='addaddress'), #增加收货地址
    path(r'orderlist/<str:goodids>/<str:goodnums>/<int:all_price>/<str:theaddress>/',OrderListView.as_view(),name='orderlist'),#确认收货地址

    path(r"favorite/",FavoriteListView.as_view(),name='favorite'),#收藏夹页面
    path(r'add_favorite/<int:good_id>/<int:nums>/',FavoriteAddView.as_view(),name='add_favorite'), #添加入收藏夹

]
