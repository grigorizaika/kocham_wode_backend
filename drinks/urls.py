from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'drinks'

urlpatterns = [
    path('user_statistics', views.user_statistics),
]