from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'preferences'

urlpatterns = [
    path('', views.PreferencesView.as_view(), name='preferences_list'),
    path('<int:id>', views.PreferencesView.as_view(), name='preferences'),
    path('<str:who>', views.PreferencesView.as_view(), name='my_preferences'),
]