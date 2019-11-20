from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    user =forms.CharField(required=True)
    pwd = forms.CharField(required=True,min_length=6)
    # 验证码
    captcha = CaptchaField()

class RegisterForm(forms.Form):
    user = forms.CharField(required=True)
    pwd = forms.CharField(required=True,min_length=6)
    repwd = forms.CharField(required=True,min_length=6)
    email = forms.EmailField(required=True)
    #验证码
    captcha = CaptchaField()

