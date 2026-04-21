from django.urls import path
from . import views

urlpatterns = [
    path('', views.checks_dashboard, name='checks_dashboard'),
    path('upload/<str:check_type>/', views.upload_check, name='upload_check'),
    path('result/<int:pk>/', views.check_result, name='check_result'),
    path('history/', views.check_history, name='check_history'),
    path('delete/<int:pk>/', views.delete_check, name='delete_check'),
]
