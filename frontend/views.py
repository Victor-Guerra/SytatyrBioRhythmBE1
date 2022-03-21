from cmath import pi
import enum
import datetime
import re
import time
from unicodedata import name
from django.shortcuts import get_object_or_404, redirect, render
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
    delete_event = request.POST.get("delete-event")
    update_event = request.POST.get("update-event")
    if delete_event:
        EventDAO().delete_event(event_id=delete_event)
        return redirect('/events/{0}'.format(user_id))
    if update_event:
        received_date = request.POST.get("updateDate")
        new_date = ""
        if received_date[-4:] == "a.m.":
            new_date = received_date.replace("a.m.", "am")
        elif received_date[-4:] == "p.m.":
            new_date = received_date.replace("p.m.", "pm")
        elif received_date[-2:] == "AM":
            new_date = received_date.replace("AM", "am")
        elif received_date[-2:] == "PM":
            new_date = received_date.replace("PM", "pm")
        datetime_object = datetime.datetime.strptime(new_date, "%B %d, %Y, %I:%M %p")
        converted_date = datetime.datetime.timestamp(datetime_object)
        received_name = request.POST.get("updateName")
        received_description = request.POST.get("updateDescription")
        received_participants = request.POST.get("updateParticipants")
        separated_participants = received_participants.split(", ")
        EventDAO().update_event(event_id=update_event, date=converted_date, name=received_name, description=received_description, participants=separated_participants)
        return redirect('/events/{0}'.format(user_id))

    events = EventDAO().get_user_events(user_id=user_id)
    for event in events:
        date1 = datetime.datetime.fromtimestamp(int(event.get('date')))        
        event.update({'date': date1.strftime("%B %d, %Y, %I:%M %p")})

    enum_events = enumerate(events)
    template = loader.get_template("frontend/events.html"); 
    context = {
        'user_id': user_id,
        'display_forecast': True,
        'enum_events': enum_events,
    }
    return HttpResponse(template.render(context, request))

# Create your views here.
