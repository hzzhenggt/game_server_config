from django.urls import path
from . import views

urlpatterns = [
    path('', views.server_list, name='server_list'),
    path('add/', views.server_add, name='server_add'),
    path('<int:pk>/edit/', views.server_edit, name='server_edit'),
    path('<int:pk>/delete/', views.server_delete, name='server_delete'),
    path('<int:pk>/', views.server_detail, name='server_detail'),
    path('server/<int:pk>/file/add/', views.server_file_add, name='server_file_add'),
    path('get_file/', views.get_file, name='get_file'),
    path('save_file/', views.save_file, name='save_file'),
    path('upload/<int:pk>/', views.upload_file, name='server_upload'),
    path('commands/', views.commands, name='commands'),
    path('command/add/', views.add_command, name='add_command'),
    path('command/edit/<int:pk>/', views.edit_command, name='edit_command'), 
    path('command/delete/<int:pk>/', views.delete_command, name='delete_command'), 
    path('command/execute/', views.handle_execute_command, name='execute_command'), 
    path('command/run/<int:pk>/', views.run_command, name='run_command'),
    #path("file_detail/<int:pk>/<str:path>/", views.file_detail, name='file_detail'),
    path('file/<int:pk>/', views.server_file_detail, name='server_file_detail'),
    #path('file/<int:pk>/', views.ServerFileDetailView.as_view(), name='server_file_detail'),
    path('file/<int:pk>/edit/', views.server_file_edit, name='server_file_edit'),
    path('file/<int:pk>/content/', views.get_file_content, name='file_content'),
    path('file/<int:pk>/deploy/', views.deploy_file, name='file_deploy'),
    path('server_files/', views.server_file_list, name='server_file_list'),
    path('serverfile/<int:pk>/delete/', views.ServerFileDeleteView.as_view(), name='server_file_delete'),
    path('compare/<int:pk>/', views.server_file_compare, name='server_file_compare'),
]


