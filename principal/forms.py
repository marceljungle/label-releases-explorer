# encoding:utf-8
from django import forms
from principal.models import ReleasesDiscogs, ReleasesBeatport


class byLabel(forms.Form):
    label = forms.CharField(label="Label name",
                            widget=forms.TextInput, required=True)


class ReleasesByDate(forms.Form):
    date = forms.CharField(
        label="Release date", widget=forms.TextInput, required=True)
