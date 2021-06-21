from django.shortcuts import render
from django.db.models import Avg, Count
from django.http.response import HttpResponseRedirect, HttpResponse
from django.conf import settings
from datetime import datetime
from principal.models import ReleasesDiscogs, ReleasesBeatport, ReleasesJuno, AllReleases
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from principal.forms import byLabel, ReleasesByDate, ReleaseByArtist, ReleaseByAlbum, byLabelAll, ReleaseByGenre
from principal.populate import populate_releases_by_label_discogs, populate_releases_by_label_beatport, populate_releases_by_label_juno, get_deezer_album_url
import re
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID, KEYWORD, NUMERIC
from whoosh.qparser import QueryParser
from whoosh.searching import Searcher
from whoosh.qparser import MultifieldParser, OrGroup
from whoosh.qparser.dateparse import DateParserPlugin
import operator
from django.db.models import Q
from functools import reduce

path = "data"

# Create your views here.


def show_releases_by_label_all(request):
    formulario = byLabelAll()
    fecha = 0
    releases = []
    page_type = "all"
    all_releases = "true"
    if request.method == 'POST':
        formulario = byLabelAll(request.POST)
        if formulario.is_valid():
            label = formulario.cleaned_data['label']
            AllReleases.objects.all().delete()
            populate_releases_by_label_beatport(label, True, 0)
            populate_releases_by_label_discogs(label, True, 0)
            populate_releases_by_label_juno(label, True, 0)
            releases = AllReleases.objects.all()
            response = redirect('/releasesall')
            return response
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL, 'page_type': page_type})


def show_releases_by_label_discogs(request):
    formulario = byLabel()
    fecha = 0
    releases = []
    page_type = "discogs"
    num = 0
    all_releases = "true"
    if request.method == 'POST':
        formulario = byLabel(request.POST)
        if formulario.is_valid():
            label = formulario.cleaned_data['label']
            num = formulario.cleaned_data['num']
            populate_releases_by_label_discogs(label, False, int(num))
            releases = ReleasesDiscogs.objects.all()
            response = redirect('/releasesdiscogs')
            return response
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL, 'page_type': page_type})


def filter_album_and_artist(album):
    artist = album.artist
    title = album.title
    if "feat" in album.artist:
        artist = re.findall(r"([\w\d\D\W]*)feat([\w\d\W]*)", album.artist)
        artist = str(artist[0][0]) + " " + str(artist[0][1])
    if "/" in album.artist:
        artist = re.findall(r"([\w\d\s]*)/", album.artist)[0]
    if " & " in album.title:
        title = re.findall(r"([\w\d\s\S]*)&", album.title)[0]
    return artist, title


def show_releases_discogs(request):
    fecha = 0
    releases = []
    page_type = "discogs"
    all_releases = "true"
    releases = ReleasesDiscogs.objects.all()
    if request.method == 'POST':
        album_id = request.POST.get('albumId', '')
        album = ReleasesDiscogs.objects.filter(id=album_id)[0]
        artist, title = filter_album_and_artist(album)
        album_and_artist = str(artist) + " " + str(title)
        get_deezer_album_url(album_and_artist)
    return render(request, 'index.html', {'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL, 'page_type': page_type})


def show_releases_beatport(request):
    formulario = byLabel()
    fecha = 0
    releases = []
    all_releases = "true"
    page_type = "beatport"
    releases = ReleasesBeatport.objects.all()
    if request.method == 'POST':
        album_id = request.POST.get('albumId', '')
        album = ReleasesBeatport.objects.filter(id=album_id)[0]
        artist, title = filter_album_and_artist(album)
        album_and_artist = str(artist) + " " + str(title)
        get_deezer_album_url(album_and_artist)
    return render(request, 'index.html', {'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL, 'page_type': page_type})


def show_releases_juno(request):
    releases = []
    all_releases = "true"
    page_type = "juno"
    releases = ReleasesJuno.objects.all()
    if request.method == 'POST':
        album_id = request.POST.get('albumId', '')
        album = ReleasesJuno.objects.filter(id=album_id)[0]
        artist, title = filter_album_and_artist(album)
        album_and_artist = str(artist) + " " + str(title)
        get_deezer_album_url(album_and_artist)
    return render(request, 'index.html', {'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL, 'page_type': page_type})


def show_releases_all(request):
    releases = []
    all_releases = "true"
    page_type = "all"
    releases = AllReleases.objects.all()
    if request.method == 'POST':
        album_id = request.POST.get('albumId', '')
        album = AllReleases.objects.filter(id=album_id)[0]
        artist, title = filter_album_and_artist(album)
        album_and_artist = str(artist) + " " + str(title)
        get_deezer_album_url(album_and_artist)
    return render(request, 'index.html', {'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL, 'page_type': page_type})


def show_releases_by_label_beatport(request):
    formulario = byLabel()
    fecha = 0
    releases = []
    page_type = "beatport"
    all_releases = "true"
    if request.method == 'POST':
        formulario = byLabel(request.POST)
        if formulario.is_valid():
            label = formulario.cleaned_data['label']
            num = formulario.cleaned_data['num']
            populate_releases_by_label_beatport(label, False, int(num))
            releases = ReleasesBeatport.objects.all()
            response = redirect('/releasesbeatport')
            return response
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL, 'page_type': page_type})


def show_releases_by_label_juno(request):
    formulario = byLabel()
    fecha = 0
    releases = []
    page_type = "juno"
    all_releases = "true"
    if request.method == 'POST':
        formulario = byLabel(request.POST)
        if formulario.is_valid():
            label = formulario.cleaned_data['label']
            num = formulario.cleaned_data['num']
            populate_releases_by_label_juno(label, False, int(num))
            releases = ReleasesJuno.objects.all()
            response = redirect('/releasesjuno')
            return response
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL, 'page_type': page_type})


def filter_by_date_beatport(request):
    formulario = ReleasesByDate()
    date = 0
    releases = []
    page_type = "beatport"
    all_releases = "false"
    if request.method == 'POST':
        try:
            album_id = request.POST.get('albumId', '')
            album = ReleasesBeatport.objects.filter(id=album_id)[0]
            artist, title = filter_album_and_artist(album)
            album_and_artist = str(artist) + " " + str(title)
            get_deezer_album_url(album_and_artist)
        except:
            formulario = ReleasesByDate(request.POST)
            if formulario.is_valid():
                date = formulario.cleaned_data['date']
                releases = ReleasesBeatport.objects.filter(
                    year__istartswith=date)
    return render(request, 'index.html', {'formulario': formulario, 'page_type': page_type, 'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_date_all(request):
    formulario = ReleasesByDate()
    date = 0
    releases = []
    page_type = "all"
    all_releases = "false"
    if request.method == 'POST':
        formulario = ReleasesByDate(request.POST)
        if formulario.is_valid():
            date = formulario.cleaned_data['date']
            releases = AllReleases.objects.filter(year__istartswith=date)
    return render(request, 'index.html', {'formulario': formulario, 'page_type': page_type, 'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_date_discogs(request):
    formulario = ReleasesByDate()
    date = 0
    releases = []
    page_type = "discogs"
    all_releases = "false"
    if request.method == 'POST':
        try:
            album_id = request.POST.get('albumId', '')
            album = ReleasesDiscogs.objects.filter(id=album_id)[0]
            artist, title = filter_album_and_artist(album)
            album_and_artist = str(artist) + " " + str(title)
            get_deezer_album_url(album_and_artist)
        except:
            formulario = ReleasesByDate(request.POST)
            if formulario.is_valid():
                date = formulario.cleaned_data['date']
                releases = ReleasesDiscogs.objects.filter(
                    year__istartswith=date)
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'page_type': page_type, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_date_juno(request):
    formulario = ReleasesByDate()
    date = 0
    releases = []
    page_type = "juno"
    all_releases = "false"
    if request.method == 'POST':
        try:
            album_id = request.POST.get('albumId', '')
            album = ReleasesJuno.objects.filter(id=album_id)[0]
            artist, title = filter_album_and_artist(album)
            album_and_artist = str(artist) + " " + str(title)
            get_deezer_album_url(album_and_artist)
        except:
            formulario = ReleasesByDate(request.POST)
            if formulario.is_valid():
                date = formulario.cleaned_data['date']
                releases = ReleasesJuno.objects.filter(year__istartswith=date)
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'page_type': page_type, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_artist_beatport(request):
    formulario = ReleaseByArtist()
    artist = ""
    releases = []
    page_type = "beatport"
    all_releases = "false"
    if request.method == 'POST':
        try:
            album_id = request.POST.get('albumId', '')
            album = ReleasesBeatport.objects.filter(id=album_id)[0]
            artist, title = filter_album_and_artist(album)
            album_and_artist = str(artist) + " " + str(title)
            get_deezer_album_url(album_and_artist)
        except:
            formulario = ReleaseByArtist(request.POST)
            if formulario.is_valid():
                artist = formulario.cleaned_data['artist']
                releases = ReleasesBeatport.objects.filter(
                    artist__contains=artist)
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'page_type': page_type, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_artist_all(request):
    formulario = ReleaseByArtist()
    artist = ""
    releases = []
    page_type = "all"
    all_releases = "false"
    if request.method == 'POST':
        try:
            album_id = request.POST.get('albumId', '')
            album = AllReleases.objects.filter(id=album_id)[0]
            artist, title = filter_album_and_artist(album)
            album_and_artist = str(artist) + " " + str(title)
            get_deezer_album_url(album_and_artist)
        except:
            formulario = ReleaseByArtist(request.POST)
            if formulario.is_valid():
                artist = formulario.cleaned_data['artist']
                releases = AllReleases.objects.filter(artist__contains=artist)
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'page_type': page_type, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_artist_discogs(request):
    formulario = ReleaseByArtist()
    artist = ""
    releases = []
    page_type = "discogs"
    all_releases = "false"
    if request.method == 'POST':
        try:
            album_id = request.POST.get('albumId', '')
            album = ReleasesDiscogs.objects.filter(id=album_id)[0]
            artist, title = filter_album_and_artist(album)
            album_and_artist = str(artist) + " " + str(title)
            get_deezer_album_url(album_and_artist)
        except:
            formulario = ReleaseByArtist(request.POST)
            if formulario.is_valid():
                artist = formulario.cleaned_data['artist']
                releases = ReleasesDiscogs.objects.filter(
                    artist__contains=artist)
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'page_type': page_type, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_artist_juno(request):
    formulario = ReleaseByArtist()
    artist = ""
    releases = []
    page_type = "juno"
    all_releases = "false"
    if request.method == 'POST':
        try:
            album_id = request.POST.get('albumId', '')
            album = ReleasesJuno.objects.filter(id=album_id)[0]
            artist, title = filter_album_and_artist(album)
            album_and_artist = str(artist) + " " + str(title)
            get_deezer_album_url(album_and_artist)
        except:
            formulario = ReleaseByArtist(request.POST)
            if formulario.is_valid():
                artist = formulario.cleaned_data['artist']
                releases = ReleasesJuno.objects.filter(artist__contains=artist)
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'page_type': page_type, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_album_juno(request):
    formulario = ReleaseByAlbum()
    album = ""
    releases = []
    page_type = "juno"
    all_releases = "false"
    if request.method == 'POST':
        try:
            album_id = request.POST.get('albumId', '')
            album = ReleasesJuno.objects.filter(id=album_id)[0]
            artist, title = filter_album_and_artist(album)
            album_and_artist = str(artist) + " " + str(title)
            get_deezer_album_url(album_and_artist)
        except:
            formulario = ReleaseByAlbum(request.POST)
            if formulario.is_valid():
                album = formulario.cleaned_data['album']
                releases = ReleasesJuno.objects.filter(title__contains=album)
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'page_type': page_type, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_album_beatport(request):
    formulario = ReleaseByAlbum()
    album = ""
    releases = []
    page_type = "beatport"
    all_releases = "false"
    if request.method == 'POST':
        try:
            album_id = request.POST.get('albumId', '')
            album = ReleasesBeatport.objects.filter(id=album_id)[0]
            artist, title = filter_album_and_artist(album)
            album_and_artist = str(artist) + " " + str(title)
            get_deezer_album_url(album_and_artist)
        except:
            formulario = ReleaseByAlbum(request.POST)
            if formulario.is_valid():
                album = formulario.cleaned_data['album']
                releases = ReleasesBeatport.objects.filter(
                    title__contains=album)
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'page_type': page_type, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_album_discogs(request):
    formulario = ReleaseByAlbum()
    album = ""
    releases = []
    page_type = "discogs"
    all_releases = "false"
    if request.method == 'POST':
        try:
            album_id = request.POST.get('albumId', '')
            album = ReleasesDiscogs.objects.filter(id=album_id)[0]
            artist, title = filter_album_and_artist(album)
            album_and_artist = str(artist) + " " + str(title)
            get_deezer_album_url(album_and_artist)
        except:
            formulario = ReleaseByAlbum(request.POST)
            if formulario.is_valid():
                album = formulario.cleaned_data['album']
                releases = ReleasesDiscogs.objects.filter(
                    title__contains=album)
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'page_type': page_type, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_album_all(request):
    formulario = ReleaseByAlbum()
    album = ""
    releases = []
    page_type = "all"
    all_releases = "false"
    if request.method == 'POST':
        try:
            album_id = request.POST.get('albumId', '')
            album = AllReleases.objects.filter(id=album_id)[0]
            artist, title = filter_album_and_artist(album)
            album_and_artist = str(artist) + " " + str(title)
            get_deezer_album_url(album_and_artist)
        except:
            formulario = ReleaseByAlbum(request.POST)
            if formulario.is_valid():
                album = formulario.cleaned_data['album']
                releases = AllReleases.objects.filter(title__contains=album)
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'page_type': page_type, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_genre_juno(request):
    formulario = ReleaseByGenre()
    genre = ""
    releases = []
    page_type = "juno"
    all_releases = "false"
    if request.method == 'POST':
        album_id = request.POST.get('albumId', 0)
        if album_id > 0:
            album = ReleasesJuno.objects.filter(id=album_id)[0]
            artist, title = filter_album_and_artist(album)
            album_and_artist = str(artist) + " " + str(title)
            get_deezer_album_url(album_and_artist)
        formulario = ReleaseByGenre(request.POST)
        if formulario.is_valid():
            genre = formulario.cleaned_data['genre']
            ix = open_dir("Index")
            with ix.searcher() as searcher:
                doc = searcher.documents()
                query = QueryParser(
                    "genre", ix.schema).parse(str(genre))
                results = searcher.search(query)
                results = [res['catalog_number'] for res in results]
                releases = ReleasesJuno.objects.filter(
                    catalog_number__in=results)
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'page_type': page_type, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def inicio(request):
    return render(request, 'index.html')


def ingresar(request):
    if request.user.is_authenticated:
        return(HttpResponseRedirect('/populate'))
    formulario = AuthenticationForm()
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        usuario = request.POST['username']
        clave = request.POST['password']
        acceso = authenticate(username=usuario, password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect('/populate'))
            else:
                return (HttpResponse('<html><body>ERROR: USUARIO NO ACTIVO </body></html>'))
        else:
            return (HttpResponse('<html><body>ERROR: USUARIO O CONTRASE&Ntilde;A INCORRECTOS </body></html>'))

    return render(request, 'ingresar.html', {'formulario': formulario})
