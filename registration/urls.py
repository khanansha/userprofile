from django.contrib import admin
from django.urls import path
from .import views
from django.conf.urls import url

urlpatterns = [
    path('' ,views.usersignup, name='register_user'),
    path('activate_email/' ,views.activate, name='register_user'),
    path('signup/',views.signup,name='signup'),
    path('otpsignup/',views.otpsignup,name='signup'),
    path('otpform/',views.otpform,name='signup'),
]