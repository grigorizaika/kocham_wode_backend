from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'drinks'

urlpatterns = [
    path('', views.DrinkView.as_view(), name='drink_list'),
    path('<int:id>', views.DrinkView.as_view(), name='drink'),
]