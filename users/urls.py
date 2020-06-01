from django.urls import path
from django.conf.urls import url

from . import views
from preferences.views import PreferencesView

app_name = 'users'

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('', views.UserView.as_view(), name='user_list'),
    path('<int:id>', views.UserView.as_view(), name='user'),
    path('<int:user_id>/preferences', PreferencesView.as_view(), name='preferences')
]