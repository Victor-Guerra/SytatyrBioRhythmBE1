from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import authenticate


def loginView(request):

    if request.method == "GET":
        display_forecast = False
        template = loader.get_template('frontend/login.html')
        context = {
            'display_forecast': display_forecast,
        }
        return HttpResponse(template.render(context, request))

    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password = password)
    
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('/')

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
