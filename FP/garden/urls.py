from django.urls import path
from . import views

urlpatterns = [
    path('', views.plant_list, name='plant_list'),
    path('<int:pk>/', views.plant_detail, name='plant_detail'),
    path('my-garden/', views.my_garden, name='my_garden'),
    path('add/<int:plant_id>/', views.add_to_garden, name='add_to_garden'),
    path('update/<int:user_plant_id>/', views.update_plant_status, name='update_plant_status'),
    path('journal/<int:user_plant_id>/', views.plant_journal, name='plant_journal'),
    path('journal/<int:user_plant_id>/add/', views.add_journal_entry, name='add_journal_entry'),

    # New Garden Features
    path('user-plant/<int:user_plant_id>/', views.user_plant_detail, name='user_plant_detail'),
    path('user-plant/<int:user_plant_id>/generate-qr/', views.generate_qr_code, name='generate_qr_code'),
    path('user-plant/<int:user_plant_id>/harvests/', views.harvest_list, name='harvest_list'),
    path('user-plant/<int:user_plant_id>/tasks/', views.task_list, name='task_list'),
    path('user-plant/<int:user_plant_id>/tasks/generate-ai/', views.generate_ai_tasks_view, name='generate_ai_tasks'),
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('user-plant/<int:user_plant_id>/health/', views.health_log_list, name='health_log_list'),
    path('expenses/', views.expense_list, name='expense_list'),
]
