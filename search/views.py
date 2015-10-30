from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from haystack.query import SearchQuerySet
from basic_parser.models import Profile, Skills
# Create your views here.

def basic(request):
    return render_to_response('search.html', {'user':auth.get_user(request)})

def new_search(request):
    args = {}

    args['user'] = auth.get_user(request)

    return render_to_response('result.html', args)