from django.urls import path
from . import views

urlpatterns = [
    path('get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),
    path('twitch/', views.getTwitchToken, name='getTwitchToken'),
    path('re_get_twitch_token/', views.reGetTwitchToken, name='reGetTwitchToken'),
]
