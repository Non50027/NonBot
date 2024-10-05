from django.urls import path
from . import views

urlpatterns = [
    path('sub/', views.sub, name='sub'),
    path('edit/', views.edit, name='edit'),
    path('get_sub/', views.get_sub, name='get_sub'),
    path('get_all_sub/', views.get_all_sub, name='get_all_sub')
]
