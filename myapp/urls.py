from django.urls import path

from .views import *

urlpatterns = [
    path('', Master.as_view()),
    path('home/', home, name='home')
]
