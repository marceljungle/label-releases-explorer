# encoding:utf-8
from django import forms
from principal.models import ReleasesDiscogs, ReleasesBeatport


class byLabel(forms.Form):
    label = forms.CharField(label="Label name",
                            widget=forms.TextInput, required=False)
    num = forms.IntegerField(label="Number of releases:",
                             widget=forms.TextInput, required=False)


class byLabelAll(forms.Form):
    label = forms.CharField(label="Label name",
                            widget=forms.TextInput, required=False)
    num = forms.IntegerField(label="Number of releases:",
                             widget=forms.TextInput, required=False)


class ReleasesByDate(forms.Form):
    date = forms.CharField(
        label="Release date", widget=forms.TextInput, required=False)


class ReleaseByArtist(forms.Form):
    artist = forms.CharField(
        label="Artist name", widget=forms.TextInput, required=False)


class ReleaseByAlbum(forms.Form):
    album = forms.CharField(
        label="Album name", widget=forms.TextInput, required=False)


class ReleaseByGenre(forms.Form):
    genre = forms.CharField(
        label="Genre name", widget=forms.TextInput, required=False)
