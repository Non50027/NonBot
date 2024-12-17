from django.urls import path
from . import views

urlpatterns = [
    path('sub/', views.sub, name='sub'),
    path('edit/', views.edit, name='edit'),
    path('get_sub/', views.get_sub, name='get_sub'),
    path('get_all_sub/', views.get_all_sub, name='get_all_sub'),
    path('set_role_message_emoji/', views.set_role_message_emoji, name= 'set_role_message_emoji'),
    path('get_role_message_emoji/', views.get_role_message_emoji, name= 'get_role_message_emoji'),
]
