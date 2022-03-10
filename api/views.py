from django.template import loader
from django.http import HttpResponse
 

# Create your views here.
def index(request):
    display_forecast = False
    template = loader.get_template('api/index.html')
    context = {
        'display_forecast': display_forecast,
    }
    return HttpResponse(template.render(context, request))

def biorhythmView(request):
    display_forecast = True
    template = loader.get_template('api/biorhythm.html')
    context = {
        'display_forecast': display_forecast,
    }
    return HttpResponse(template.render(context, request))

def loginView(request):
    pass

def signupView(request):
    pass
