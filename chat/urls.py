from django.urls import path
from .views import interface_english, interface_arabic, home

urlpatterns = [
    path('chat/arabic/', interface_arabic, name='interface_arabic'),
    path('chat/english/', interface_english, name='interface_english'),
    path('', home, name='home')
]
