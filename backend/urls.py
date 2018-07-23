
from django.urls import path, include
from .views import get, initialize, arabic_get, arabic_initialize

urlpatterns = [
    path('arabic/get/', arabic_get, name='arabic_get'),
    path('arabic/initialize/', arabic_initialize, name='arabic_initialize'),
    path('get/', get, name='get'),
    path('initialize/', initialize, name='initialize')
]
