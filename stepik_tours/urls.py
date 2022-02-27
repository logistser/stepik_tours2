"""stepik_tours URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from tours.views import main_view, departure_view, tour_view, tour_purchase

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main'),
    path('departure/<str:departure>/', departure_view, name='departure'),
    path('tour/<int:id>/', tour_view, name='tour'),
    path('buy/', tour_purchase, name='purchase'),
]
