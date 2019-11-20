"""briupshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('goods/',include('goods.urls',namespace='goods')),  #命名空间 反向解析
    path('users/',include('users.urls',namespace='users')),
    path('operations/',include('operations.urls',namespace='operations')),
    url(r'^captcha/', include('captcha.urls')),  # 验证码
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
