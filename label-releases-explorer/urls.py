"""label-releases-explorer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from principal import views
from principal import populate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio),
    path('ingresar/', views.ingresar),
    path('carga/', populate.populateDatabase),
    path('inicio/', views.inicio),
    path('releasesbylabelbeatport/', views.show_releases_by_label_beatport),
    path('releasesbylabeldiscogs/', views.show_releases_by_label_discogs),
    path('releasesbylabeljuno/', views.show_releases_by_label_juno),
    path('releasesdiscogs/', views.show_releases_discogs),
    path('releasesbeatport/', views.show_releases_beatport),
    path('releasesjuno/', views.show_releases_juno),
    path('filterbydatebeatport/', views.filter_by_date_beatport),
    path('filterbydatediscogs/', views.filter_by_date_discogs),
    path('filterbydatejuno/', views.filter_by_date_juno),
]
