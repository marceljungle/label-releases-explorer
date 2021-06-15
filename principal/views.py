from django.shortcuts import render
from django.db.models import Avg, Count
from django.http.response import HttpResponseRedirect, HttpResponse
from django.conf import settings
from datetime import datetime
from principal.models import ReleasesDiscogs, ReleasesBeatport, ReleasesJuno
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from principal.forms import byLabel, ReleasesByDate
from principal.populate import populate_labels_by_discogs, populate_releases_by_label_beatport, populate_labels_by_juno

path = "data"

# Create your views here.


def show_releases_by_label_discogs(request):
    formulario = byLabel()
    fecha = 0
    releases = []
    page_type = "discogs"
    all_releases = "true"
    if request.method == 'POST':
        formulario = byLabel(request.POST)
        if formulario.is_valid():
            label = formulario.cleaned_data['label']
            populate_labels_by_discogs(label)
            releases = ReleasesDiscogs.objects.all()
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL, 'page_type': page_type})


def show_releases_discogs(request):
    formulario = byLabel()
    fecha = 0
    releases = []
    page_type = "discogs"
    all_releases = "true"
    releases = ReleasesDiscogs.objects.all()
    return render(request, 'index.html', {'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL, 'page_type': page_type})


def show_releases_beatport(request):
    formulario = byLabel()
    fecha = 0
    releases = []
    all_releases = "true"
    page_type = "beatport"
    releases = ReleasesBeatport.objects.all()
    return render(request, 'index.html', {'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL, 'page_type': page_type})


def show_releases_juno(request):
    formulario = byLabel()
    fecha = 0
    releases = []
    all_releases = "true"
    page_type = "juno"
    releases = ReleasesJuno.objects.all()
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
            populate_releases_by_label_beatport(label)
            releases = ReleasesBeatport.objects.all()
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
            populate_labels_by_juno(label)
            releases = ReleasesJuno.objects.all()
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL, 'page_type': page_type})


def filter_by_date_beatport(request):
    formulario = ReleasesByDate()
    date = 0
    releases = []
    page_type = "beatport"
    all_releases = "false"
    if request.method == 'POST':
        formulario = ReleasesByDate(request.POST)
        if formulario.is_valid():
            date = formulario.cleaned_data['date']
            releases = ReleasesBeatport.objects.filter(year__istartswith=date)
    return render(request, 'index.html', {'formulario': formulario, 'page_type': page_type, 'releases': releases, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_date_discogs(request):
    formulario = ReleasesByDate()
    date = 0
    releases = []
    page_type = "discogs"
    all_releases = "false"
    if request.method == 'POST':
        formulario = ReleasesByDate(request.POST)
        if formulario.is_valid():
            date = formulario.cleaned_data['date']
            releases = ReleasesDiscogs.objects.filter(year__istartswith=date)
    return render(request, 'index.html', {'formulario': formulario, 'releases': releases, 'page_type': page_type, 'all_releases': all_releases, 'STATIC_URL': settings.STATIC_URL})


def filter_by_date_juno(request):
    formulario = ReleasesByDate()
    date = 0
    releases = []
    page_type = "discogs"
    all_releases = "false"
    if request.method == 'POST':
        formulario = ReleasesByDate(request.POST)
        if formulario.is_valid():
            date = formulario.cleaned_data['date']
            releases = ReleasesJuno.objects.filter(year__istartswith=date)
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
