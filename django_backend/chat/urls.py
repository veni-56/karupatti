from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('<int:conversation_id>/send/', views.send_message, name='send_message'),
    path('<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('start/<int:shop_id>/', views.start_conversation, name='start_conversation'),
    path('unread-count/', views.get_unread_count, name='unread_count'),
]
