from django.contrib import admin
from django.urls import path
from accounts import views
from django.conf.urls import url,include
urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("logout",views.logoutUser,name='logout'),
    path('register' , views.register_attempt , name="register_attempt"),
    path('accounts/login/' , views.login_attempt , name="login_attempt"),
    path('token' , views.token_send , name="token_send"),
    path('success' , views.success , name='success'),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('error' , views.error_page , name="error")

    
   
]
