from django.urls import path
from . import views


urlpatterns =[
    path('', views.home, name= 'home'),

    #Auth built in on Django
path('register/', views.register_user, name='register'),
path('login/', views.login_user, name='login'),
path('logout/', views.logout_user, name ='logout'),
#Task creation and list
path('list/', views.task_list, name='task_list'),
path('create/', views.task_create, name='task_form'),
path('edit/<int:pk>/', views.task_edit, name='task_edit'),
path('delete/<int:pk>/', views.task_delete, name='task_delete'),

]