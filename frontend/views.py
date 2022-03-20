from collections import UserList
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import authenticate
from .firebase.firebase import init_firebase
from .firebase.firebase import create_user
from .firebase.firebase import get_user
from .firebase.login import get_user_check
from django.contrib import messages
from passlib.hash import django_pbkdf2_sha256

init_firebase()

def loginView(request):

    if request.method == "GET":
        display_forecast = False
        template = loader.get_template('frontend/login.html')
        context = {
            'display_forecast': display_forecast,
        }
        return HttpResponse(template.render(context, request))

    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user, isvalid = get_user_check(email, password)
        #print(enc_password)
        if isvalid:
           print("Logged in successfully")
           return redirect(f'/biorhythm/{user["id"]}')
        else: 
           print("Invalid Passwords")
           messages.error(request,'Invalid Credentials, please try again')
           return redirect('/')
       
        #user = authenticate(username=username,password = password)
        #if user is not None:
        #    auth.login(request, user)
        #    return redirect('/')
        #else:
        #    messages.info(request, 'invalid credentials')
        #    return redirect('/')

def signupView(request):
    display_forecast = False
    template = loader.get_template('frontend/base.html')
    context = {
        'display_forecast': display_forecast,
    }
    return HttpResponse(template.render(context, request))

    pass

def biorhythmView(request, user_id =0):
    if(user_id == 0):
        raise Http404("Invalid user_id.")

    template = loader.get_template("frontend/base.html"); 
    context = {
        'display_forecast': True
    }
    return HttpResponse(template.render(context, request))

def schedulerView(request):
    pass

def eventList(request):
    pass

# Create your views here.
