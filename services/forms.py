from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

CITY_CHOICES = [
    ('', 'شهر خود را انتخاب کنید'),
    ('تهران', 'تهران'),
    ('مشهد', 'مشهد'),
    ('اصفهان', 'اصفهان'),
    ('شیراز', 'شیراز'),
    ('تبریز', 'تبریز'),
    ('کرج', 'کرج'),
    ('قم', 'قم'),
    ('اهواز', 'اهواز'),
    ('رشت', 'رشت'),
    ('کرمانشاه', 'کرمانشاه'),
    ('زاهدان', 'زاهدان'),
    ('ارومیه', 'ارومیه'),
]


class LoginForm(forms.Form):
    username = forms.CharField(
        label='نام کاربری',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری خود را وارد کنید'})
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور خود را وارد کنید'})
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='ایمیل')
    city = forms.CharField(
        label='شهر محل سکونت',
        max_length=100,
        widget=forms.Select(choices=CITY_CHOICES)
    )
    neighborhood = forms.CharField(
        label='محله',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'مثال: سعادت‌آباد، ونک، ...'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'city', 'neighborhood']