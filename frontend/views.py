from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.views import View

from . import brcalc


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

class BiorhythmView(View):
    display_br = False
    display_brfc = False
    br_plot = ""
    brfc_plot = ""
    
    def get(self, request, user_id=0):
        self.display_br = False
        if(user_id == 0):
            raise Http404("Invalid user_id.")
        # user = Object.User.findById(user_id)

        do_disp_br = request.GET.get("load-br")
        do_disp_brfc = request.GET.get("load-brfc")
        go_back = request.GET.get("go-back")

        if do_disp_br:
            self.display_br = True
            self.display_brfc = False
            if self.br_plot == "":
                self.br_plot = brcalc.calcBR(1000, 150) 
        elif do_disp_brfc:
            self.display_br = False
            self.display_brfc = True
            if self.brfc_plot == "":
                self.brfc_plot = brcalc.calcBRFC(1000, 150) 
        else:
            self.display_br = False
            self.display_brfc = False
            
        
        context = {
                'user_id': user_id,
                #'user_img': user_img,
                'user_birthdate': '06-10-2000',
                #'user_functions': user_functions,
                'display_br': self.display_br,
                'display_brfc': self.display_brfc,
                'br_plot': self.br_plot,
                'brfc_plot': self.brfc_plot,
        }
        
        return render(request, "frontend/biorhythm/biorhythm.html", context)
    


def schedulerView(request):
    pass

def eventList(request):
    pass

# Create your views here.
