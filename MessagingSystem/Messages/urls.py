from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users),
    path('users/<int:user_id>/', views.specific_user),
    path('messages/', views.messages),
    path('messages/<int:message_id>/', views.specific_message),
    path('all-messages/<int:user_id>/', views.all_user_messages),
    path('unread-messages/<int:user_id>/', views.all_user_unread_messages),
    path('read-messages/<int:message_id>/', views.read_message)
]
