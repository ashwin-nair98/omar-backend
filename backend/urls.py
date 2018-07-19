
from django.urls import path, include
from .views import get, initialize

urlpatterns = [
    path('get/', get, name='get'),
    path('initialize/', initialize, name='initialize')
]