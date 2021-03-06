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
    path('releasesbylabelall/', views.show_releases_by_label_all),
    path('releasesdiscogs/', views.show_releases_discogs),
    path('releasesbeatport/', views.show_releases_beatport),
    path('releasesjuno/', views.show_releases_juno),
    path('releasesall/', views.show_releases_all),
    path('filterbydatebeatport/', views.filter_by_date_beatport),
    path('filterbydatediscogs/', views.filter_by_date_discogs),
    path('filterbydatejuno/', views.filter_by_date_juno),
    path('filterbydateall/', views.filter_by_date_all),
    path('filterbyartistjuno/', views.filter_by_artist_juno),
    path('filterbyartistbeatport/', views.filter_by_artist_beatport),
    path('filterbyartistdiscogs/', views.filter_by_artist_discogs),
    path('filterbyartistall/', views.filter_by_artist_all),
    path('filterbyalbumjuno/', views.filter_by_album_juno),
    path('filterbyalbumbeatport/', views.filter_by_album_beatport),
    path('filterbyalbumdiscogs/', views.filter_by_album_discogs),
    path('filterbyalbumall/', views.filter_by_album_all),
    path('filterbygenrejuno/', views.filter_by_genre_juno)
]
