from django.urls import path,include
from .views import *

app_name = '[goods]'  #反向解析

urlpatterns = [
    # path(r"login/",user_login,name='login'),  # 函数视图配置
    path(r"login/",LoginView.as_view(),name='login'),
    path(r"logout/",LogoutView.as_view(),name='logout'),
    # path(r"register/",user_register,name='register'),
    path(r"register/",Register.as_view(),name='register'),
    path(r"userinfo/",UserInfoView.as_view(),name='userinfo'), #修改用户信息
]
