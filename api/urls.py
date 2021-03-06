from django.urls import path, include
from django.conf.urls import url

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import generics, permissions

from . import views

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0),),
    path('users/', include('users.api_urls', namespace='users')),
    path('preferences/', 
         include('preferences.api_urls', namespace='preferences')),
    path('drinks/', include('drinks.api_urls', namespace='drinks')),

    path('confirm_sign_up/', views.confirm_sign_up, name='confirm-sign-up'),
    path('resend_confirmation_code/', views.resend_confirmation_code, name='resend-confirmation-code'),
    path('change_password/', views.change_password, name='change-password'),
    path('get_tokens/', views.get_jwt_tokens, name='get-tokens'),
    path('refresh_tokens/', views.refresh_jwt_tokens, name='refresh-tokens'),
]