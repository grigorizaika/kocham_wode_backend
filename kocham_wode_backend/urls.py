"""kocham_wode_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import url 
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import start

urlpatterns = [
    path('', start),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', auth_views.LogoutView.as_view()),

    path('api/', include('api.urls', namespace='api')),
    path('drinks/', include('drinks.urls', namespace="drinks")),

] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
