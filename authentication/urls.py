from django.contrib import admin
from django.urls import path
from authentication import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("login",views.loginaction,name="login"),
    path("signup",views.signup,name="signup"),
    path("login-page",views.renderlogin,name="login-page"),
    path("signup-page",views.rendersignup,name="signup-page"),
    path('logout', views.logoutuser, name='logout'),

]
