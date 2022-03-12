from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404

def index(request, user_id=0):
    template = loader.get_template("frontend/base.html")
    context = { #props
        'user_id': user_id,
    }
    return HttpResponse(template.render(context, request))

def loginView(request):
    pass

def signupView(request):
    pass

def biorhythmView(request, user_id =0):
    if(user_id == 0):
        raise Http404("Invalid user_id.")
    # user = Object.User.findById(user_id)
    template = loader.get_template("frontend/biorhythm/biorhythm.html"); 
    context = {
            'user_id': user_id,
            #'user_img': user_img,
            #'user_birthdate': user_birthdate,
            #'user_functions': user_functions,
            'display_br': False,
            'display_brfc': False
    }
    return HttpResponse(template.render(context, request))

def schedulerView(request):
    pass

def eventList(request):
    pass

# Create your views here.
