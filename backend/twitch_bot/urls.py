from django.urls import path
from . import views

urlpatterns = [
    path('get_all_channel_data/', views.get_all_channel_data, name= 'get_all_channel_data'),
]
