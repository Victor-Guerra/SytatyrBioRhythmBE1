from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def loginView(request):
    display_forecast = False
    template = loader.get_template('api/index.html')
    context = {
        'display_forecast': display_forecast,
    }
    return HttpResponse(template.render(context, request))


def signupView(request):
    pass

def biorhythmView(request):
    pass

def schedulerView(request):
    pass

def eventList(request):
    pass

# Create your views here.
