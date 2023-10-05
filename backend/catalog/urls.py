"""
URL configuration for catalog app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from .views import HomeView, CategoryView, CategoryGroupView, AutoPartView, handler404


handler404 = handler404
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('catalog/category_group/<slug:slug>/', CategoryGroupView.as_view(), name='category_group'),
    path('catalog/category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('catalog/auto_part/<str:number>/', AutoPartView.as_view(), name='auto_part'),
]
