from django.urls import path
from . import views

urlpatterns = [
    path('audit/', views.home, name='home'),
    path('task/', views.all_task, name='task'),
    path('task/<int:task_id>/toggle/', views.toggle_task, name='toggle_task'),
    path('add/', views.add_task, name='add'),
    path('<int:task_id>/edit/', views.edit_task, name='edit'),
    path('<int:task_id>/delete/', views.delete_task, name='delete'),
    path('register/', views.register, name='register'),
    path('log_out/', views.user_logout, name='log_out'),
    path('search/', views.search, name='search'),
]