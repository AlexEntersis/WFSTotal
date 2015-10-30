__author__ = 'Alex'
from django import forms



class NameForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    login = forms.CharField(label='login', max_length=100)
    password = forms.CharField(label='password', max_length=100)