from django.shortcuts import render

# Create your views here.

from django.contrib import auth
from django.shortcuts import redirect, render_to_response

def password_reset_done(request):
    return  render_to_response('statistics.html')

def login(request):
    args = {}

    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)

def logout(request):
    auth.logout(request)
    return redirect('/')
