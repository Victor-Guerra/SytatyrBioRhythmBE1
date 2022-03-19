import enum
import datetime
import time
from unicodedata import name
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from .firebase.firebase import init_firebase
from .firebase.firebase import create_user
from .firebase.firebase import get_user
from .firebase.events import EventDAO

init_firebase()
# get_user()
# user = {
#     "username": "EL kiko",
#     "email": "kike@tristin.com"
# }
# create_user(user)
# create_user()

#from ..api.models import Event

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

    template = loader.get_template("frontend/biorhythm.html"); 
    context = {
        'display_forecast': True
    }
    return HttpResponse(template.render(context, request))

def schedulerView(request):
    pass

def eventList(request, user_id):
    events = EventDAO().get_user_events(user_id=user_id)
    for event in events:
        event.update({'date': datetime.datetime.fromtimestamp(int(event.get('date')))})

    enum_events = enumerate(events)
    template = loader.get_template("frontend/events.html"); 
    context = {
        'display_forecast': True,
        'enum_events': enum_events,
    }
    return HttpResponse(template.render(context, request))

# Create your views here.
