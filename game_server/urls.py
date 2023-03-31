from django.urls import path
from . import views

urlpatterns = [
    path('', views.server_list, name='server_list'),
    path('add/', views.server_add, name='server_add'),
    path('<int:pk>/edit/', views.server_edit, name='server_edit'),
    path('<int:pk>/delete/', views.server_delete, name='server_delete'),
    path('<int:pk>/', views.server_detail, name='server_detail'),
    path('list_files/', views.list_files, name='list_files'),
    path('get_file/', views.get_file, name='get_file'),
    path('save_file/', views.save_file, name='save_file'),
    path('run_command/', views.run_command, name='run_command'),
]
