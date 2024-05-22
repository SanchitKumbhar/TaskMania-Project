from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path('manager_panel', views.manager_panel, name='manager_panel'),
    path('employee_panel', views.employee_panel, name='employee_panel'),
    path('signup_manager', views.signup_mamanger, name='signup_mamanger'),
    path('signup_employee', views.signup_employee, name='signup_employee'),
    path('login_employee', views.loginuser_employee, name='login_employee'),
    path('login_manager', views.loginuser_manager, name='loginuser_manager'),
    path('logout', views.logoutuser, name='logout'),
    path('taskdone/<int:id>', views.taskdone, name='taskdone'),
    path('delete-todo/<int:id>', views.delete, name='delete'),
    path('visualization', views.visualization, name='visualization'),
    path('visualization/<str:username>/', views.subvisualization, name='subvisualization'),
    path('employee', views.employee, name='employee'),
    path('manager', views.manager, name='manager'),
    path('', views.index, name=''),
    path('Authentication', views.Authentication, name='Authentication'),
]
