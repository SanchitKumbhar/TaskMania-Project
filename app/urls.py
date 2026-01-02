from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('taskdone/<int:id>', views.taskdone, name='taskdone'),
    path('delete-todo/<int:id>', views.delete, name='delete'),
    path('visualization', views.visualization, name='visualization'),
    path('visualization/<str:username>/', views.subvisualization, name='subvisualization'),
    path('employee', views.employee, name='employee'),
    path('manager-panel', views.manager, name='manager'),
    path('', views.index, name=''),
    path("profile",views.profilepage,name="profile"),
    path("show-tasks-info",views.showTasksinfo,name="show-tasks-info"),
    # path("Task-Forward",views.TaskForward,name="Task-Forward"),
    path("allocate-task/api",views.forwardTaskapi,name="allocate-task/api"),
    path("all-tasks",views.allTasks,name="all-tasks"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
