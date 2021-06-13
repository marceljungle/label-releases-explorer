# encoding:utf-8
from django import forms
from principal.models import ReleasesDiscogs, ReleasesBeatport


class byLabel(forms.Form):
    label = forms.CharField(label="Label name",
                            widget=forms.TextInput, required=True)
