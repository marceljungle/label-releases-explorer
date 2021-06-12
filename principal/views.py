from django.shortcuts import render
from django.db.models import Avg, Count
from django.http.response import HttpResponseRedirect, HttpResponse
from django.conf import settings
from datetime import datetime
from principal.models import Release
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from principal.forms import byLabel
from principal.populate import populate_labels_by_discogs

path = "data"

# Create your views here.


def show_releases_by_label(request):
    formulario = byLabel()
    fecha = 0
    releases = []
    if request.method == 'POST':
        formulario = byLabel(request.POST)
        if formulario.is_valid():
            releasesList = Release.objects.all()
            label = formulario.cleaned_data['label']
            populate_labels_by_discogs(label)
            releases = Release.objects.all()
    return render(request, 'releases.html', {'formulario': formulario, 'releases': releases, 'STATIC_URL': settings.STATIC_URL})


def inicio(request):
    return render(request, 'inicio.html')


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
