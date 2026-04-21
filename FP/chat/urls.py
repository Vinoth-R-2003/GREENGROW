from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversations, name='conversations'),
    path('<int:user_id>/', views.chat_room, name='chat_room'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
]
