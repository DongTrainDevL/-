"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import authenticate, login as authlogin
from django.contrib.auth import logout as authlogout

urlpatterns = [
    
    path("", include("myapp.urls")),
    path('admin-myadmintrator/', include(('myadmintrator.urls', 'myadmintrator'), namespace='admin-myadmintrator')),
    path("admin/", admin.site.urls),
]
