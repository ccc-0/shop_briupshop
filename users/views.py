from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import UserInfo
from .forms import LoginForm,RegisterForm
from  django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password  #django加密方式
from django.http import HttpResponseRedirect

# Create your views here.
#函数视图：dbv  类视图 cbv

def user_login(request):
    if request.method == 'GET': #判断请求方式
        return render(request,'login.html',{ })
    else:
        #表单验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            #接收数据
            user_name = request.POST.get('user','')
            user_pwd = request.POST.get('pwd','')
            # authenticate 验证用户名和密码是否匹配
            user = authenticate(username = user_name,password = user_pwd)
            if user is not None:
                login(request,user)
                return render(request,'index.html')
            else:
                return render(request,'login.html',{})
        else:
            return render(request, 'login.html', {"login_form":login_form})

class LoginView(View):
    def get(self,request ):# GET请求
        login_form = RegisterForm()
        return render(request, 'login.html', {'login_form': login_form})
    def post(self,request): #POST请求
        # 表单验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 接收数据
            user_name = request.POST.get('user', '')
            # user_name = request.POST['']  #两种方式
            user_pwd = request.POST.get('pwd', '')
            # authenticate 验证用户名和密码是否匹配
            user = authenticate(username=user_name, password=user_pwd)
            if user is not None:
                login(request, user)
                #重定向   两种：HttpResposeRedirect  / redirext
                # return HttpResponseRedirect('/goods/index/') # /代表从根目录开始
                # return redirect('/goods/index')
                url = reverse('goods:index')  #反向解析
                return redirect(url)

                # return render(request, 'index.html')
            else:
                return render(request, 'login.html', {})
        else:
            return render(request, 'login.html', {"login_form": login_form})

# 注销
class LogoutView(View):
    def get(self,request):
        logout(request)
        return render(request,'login.html')


def user_register(request):
    return render(request,'register.html',{ })

class Register(View):
    def get(self, request):
        res_form = RegisterForm()
        return render(request,'register.html',{ 'res_form': res_form})
    def post(self,request):
        # 表单验证
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
        #  接收数据 （form active method  按钮-submit  文件-entypepost multipart/from-data））
            user_name = request.POST.get('user', '')
            user_pwd = request.POST.get('pwd', '')
            user_repwd = request.POST.get('repwd','')
            user_email = request.POST.get('email','')
            # 逻辑判断  密码==重复密码
            if user_repwd == user_pwd:
                # # 将密码进行加密 make_password(pwd)
                # user_pwd= make_password(user_pwd)
                # newuser = User(username=user_name, password=user_pwd,email=user_email)
                # if newuser is not None:
                #     # 保存数据 （）
                #     #         t = TypeInfo()
                #     #         t.tname = tname
                #     #         t.save
                #     newuser.save()
                #     return render(request, 'login.html')
                # else:
                #     return render(request, 'register.html', {})
                newuser = User()
                newuser.username = user_name  # 唯一
                newuser.password = make_password(user_repwd)  # 加密
                newuser.email = user_email
                newuser.save()  # 需要进行异常捕获
                return render(request,'login.html')
            else:
                return render(request,'register.html',context={'error':'两次输入密码不一样'})
        else:
            return render(request, 'register.html', {"register_form": register_form})

class UserInfoView(View):
    def get(self,request):
        #判断是否登录

        # 获取数据：性别 头像
        try:
            userinfo = UserInfo.objects.get(user=request.user)
        except Exception as e:
            userinfo = []
        return render(request,'member_info.html',{
            'userinfo':userinfo,
        })
    def post(self,request):
        #处理数据
        truename = request.POST.get('truename','')

        #存储真实姓名
        userbase = User.objects.get(pk=request.user.id)
        userbase.last_name =truename
        userbase.save()

        gender = request.POST.get('sex','')
        try:   #更新数据
            userinfo = UserInfo.objects.get(user=request.user)
            userinfo.gender = gender
            #判断用户是否选择了图片
            userphoto = request.FILES.get('userphoto','')
            if userphoto:
                userinfo.userphoto=userphoto
            userinfo.save()
        except :  #第一次完事新增数据
            userphoto = request.FILES.get('userphoto', '')
            if userphoto:
                u = UserInfo.objects.create(gender=gender,userphoto=userphoto,user=request.user)
            else:
                u = UserInfo.objects.create(gender=gender,userphoto='/upload/默认',user=request.user)
            u.save()

        return redirect(reverse('users:userinfo'))
