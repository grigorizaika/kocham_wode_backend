from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'users'

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('', views.UserView.as_view(), name='users'),
    path('<int:id>', views.UserView.as_view(), name='user'),
]