from collections import UserList
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import authenticate
#from .firebase.firebase import init_firebase
#from .firebase.firebase import create_user
#from .firebase.firebase import get_user
from .firebase.login import get_user_check
from django.contrib import messages
from passlib.hash import django_pbkdf2_sha256
from .firebase.firebase import userDao
from django.views import View
from . import brcalc
from . import modelvalidate as mv


#init_firebase()

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

class BiorhythmView(View):
    display_br = False
    display_brfc = False
    br_plot = ""
    brfc_plot = ""
    
    def get(self, request, user_id=0):
        from datetime import datetime

        user = userDao().get_user_by_id(id=user_id)
        if mv.userValidate.is_valid(user):

            user_bd = datetime.strptime(user['birthday'], '%d-%m-%Y')
            hoy = datetime.today()

            do_disp_br = request.GET.get("load-br")
            do_disp_brfc = request.GET.get("load-brfc")
            go_back = request.GET.get("go-back")

            if do_disp_br:
                self.display_br = True
                self.display_brfc = False
                if self.br_plot == "":
                    self.br_plot = brcalc.calcBR(user_bd, hoy) 
            elif do_disp_brfc:
                self.display_br = False
                self.display_brfc = True
                if self.brfc_plot == "":
                    self.brfc_plot = brcalc.calcBRFC(user_bd, hoy) 
            else:
                self.display_br = False
                self.display_brfc = False
            
            context = {
                    'user_id': user_id,
                    'user_img': user['profilePicture'],
                    'user_birthdate': user_bd.strftime('%d-%m-%Y'),
                    'today_date': hoy.strftime('%d-%m-%Y'),
                    'display_br': self.display_br,
                    'display_brfc': self.display_brfc,
                    'br_plot': self.br_plot,
                    'brfc_plot': self.brfc_plot,
            }
            return render(request, "frontend/biorhythm/biorhythm.html", context)
        else:
            raise Http404("Invalid User")


def schedulerView(request):
    pass

def eventList(request):
    pass

# Create your views here.
