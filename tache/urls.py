from django.contrib import admin
from django.urls import path, include
from django.urls import path
from . import views
from .views import signup
from .views import login_view
urlpatterns = [
    path('', views.home, name='home'),  
    path('update-profile/', views.update_profile, name='update_profile'),
    path('create-project/', views.create_project, name='create_project'),
    path('projects/', views.project_list, name='project_list'),
    path('create-task/', views.create_task, name='create_task'),
    path('tasks/', views.task_list, name='task_list'),
    path('statistics/', views.statistics, name='statistics'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('profile/', views.profile, name='profile'),

]
