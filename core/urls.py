from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('politica/', politica, name='politica'),
]
