import enum
from unicodedata import name
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404

from frontend.models import Destination
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

def eventList(request):
    event1 = {
        'date': '31 Dic',
        'title': 'La Santa Inquisición',
        'description': 'Erase una vez',
        'participants': ['Juan', 'Santiago', 'Pedro']
    }

    event2 = {
        'date': '02 Nov',
        'title': 'Come Caca Eddy',
        'description': 'Un hombre llamado',
        'participants': ['Maria', 'Gabriel', 'Herodes', 'Roberto']
    }

    event3 = {
        'date': '02 Nov',
        'title': 'XDXDXD XDXDXD XDXDXDX',
        'description': 'Un hombre llamado',
        'participants': ['Maria', 'Gabriel']
    }

    events = [event1, event2, event3]
    enum_events = enumerate(events)
    template = loader.get_template("frontend/events.html"); 
    context = {
        'display_forecast': True,
        'events': events,
        'enum_events': enum_events,
    }
    return HttpResponse(template.render(context, request))

# Create your views here.
