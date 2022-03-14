from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from .firebase.firebase import init_firebase
from .firebase.firebase import create_user
from .firebase.firebase import get_user


init_firebase()
get_user()
# user = {
#     "username": "EL kiko",
#     "email": "kike@tristin.com"
# }
# create_user(user)
create_user()

def index(request, user_id=0):
    template = loader.get_template("frontend/base.html")
    context = { #props
        'user_id': user_id,
    }
    return HttpResponse(template.render(context, request))
    
def loginView(request):
    display_forecast = False
    template = loader.get_template('api/index.html')
    context = {
        'display_forecast': display_forecast,
    }
    return HttpResponse(template.render(context, request))


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
