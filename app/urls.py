from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('employee-panel', views.employee_panel, name='employee_panel'),
    path('signup_manager', views.signup_manager, name='signup_mamanger'),
    path('signup_employee', views.signup_employee, name='signup_employee'),
    path('employee-login', views.loginuser_employee, name='login_employee'),
    path('logout', views.logoutuser, name='logout'),
    path('taskdone/<int:id>', views.taskdone, name='taskdone'),
    path('delete-todo/<int:id>', views.delete, name='delete'),
    path('visualization', views.visualization, name='visualization'),
    path('visualization/<str:username>/', views.subvisualization, name='subvisualization'),
    path('employee', views.employee, name='employee'),
    path('manager-panel', views.manager, name='manager'),
    path('', views.index, name=''),
    path('Authentication', views.Authentication, name='Authentication'),
    path('Authentication/login-manager', views.managerloginpage, name='Authentication/login-manager'),
    path('Authentication/login-employee', views.employeelogin, name='Authentication/login-employee'),
    path('manager-login', views.managerlogin, name='credentials-login'),
    path("profile",views.profilepage,name="profile"),
    path("login-page",views.loginpage,name="login-page"),
    path("signup-page",views.signuppage,name="signup-page")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
