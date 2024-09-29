from django.urls import path
from . import views

urlpatterns = [
    path('get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),
    path('twitch/', views.get_twitch_token, name='get_twitch_token'),
    path('re_get_twitch_token/', views.re_get_twitch_token, name='re_get_twitch_token'),
    path('check_twitch_token/', views.check_twitch_token, name='check_twitch_token'),
]
