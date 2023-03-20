from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('parse', parse),
    path('getOne', get_one),
    path('accept', accept),
    path('reject', reject),
    path('getNext', get_next),
    path('download', download),
    path('trim', trim)
]
