# -*- coding: utf8 -*-

from django import forms


class PersonImageForm(forms.Form):
    name = forms.CharField()
    image = forms.ImageField()
