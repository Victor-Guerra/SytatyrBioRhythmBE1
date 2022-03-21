import os
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.contrib import messages
from django.views import View
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from google.cloud import storage as gs
from pathlib import Path
from os import path
from firebase_admin import storage
from passlib.hash import django_pbkdf2_sha256
from .firebase.login import get_user_check
from .firebase.signup import post_users
from .firebase.firebase import userDao
from datetime import datetime
import requests

from . import brcalc
from . import modelvalidate as mv


#PATH for Google Credentials
myfilepath = settings.BASE_DIR / "frontend/firebase/serviceAccountKey.json"
def_path = str(path.realpath(myfilepath))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = def_path

#PATH for Profile Picture Image
myprofilepic_path = Path(Path(__file__).resolve()).parent 
defprofilepic_path = str(path.realpath(myprofilepic_path))

#Upload Files to Storage
def upload_blob(bucket_name, source_file_name, destination_blob_name):

    storage_client = gs.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    #Requests the file using the public url
    r = requests.head(blob.public_url)
    #Whether the file exists or not on the server
    fileExists = (r.status_code == requests.codes.ok)
    fileExists = blob.exists()
    if fileExists:
        return 'Image already exists, please change the file name.'

    blob.upload_from_filename(source_file_name)

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

class SignupView(View):
    signup_redirect = '/signup'
    bucket_name='biorhythmsytatyr.appspot.com'  

    def get(self, request):
        template = loader.get_template('frontend/signup.html')
        context = {
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        try:
            username = request.POST['username']
            email = request.POST['email']
            birthday = request.POST['birthday']
            profilePicture = request.FILES['profilePicture']
            password = request.POST['password']
            
            if username =="" or email =="" or birthday=="" or password=="":
                messages.error(request,'There is one or more empty fields!')
                return redirect(self.signup_redirect)
            elif profilePicture == "":
                return redirect(self.signup_redirect)
            else:
                try:
                    datetime.strptime(birthday,"%d-%m-%Y")
                except ValueError: 
                    messages.error(request,'Format of date is not correct')
                    return redirect(self.signup_redirect)


            # Check if the given email is available
            user = userDao().get_user_by_email(email)
            if user:
                messages.error(request, "Email is already registered.")
                return redirect(self.signup_redirect)
            
            # Check if the given filename for the profile picture already exists
            fss = FileSystemStorage()
            if not fss.exists(profilePicture.name):
                # If the file already exists, do not save it
                file = fss.save(profilePicture.name, profilePicture)
            

                
            img_path = settings.BASE_DIR / 'media/' / profilePicture.name
                 
            # Check if the given filename for the profile picture already exists
            # in the google cloud storage
            if err := upload_blob(self.bucket_name, img_path, profilePicture.name):
                messages.error(request,err)
                return redirect(self.signup_redirect)

            # Encrypt password
            enc_password = django_pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
            post_users(username, email, birthday, profilePicture.name, enc_password)

            return redirect('/')    

        except KeyError:
            messages.error(request,'Please upload an image')
            return redirect(self.signup_redirect)

class BiorhythmView(View):
    display_br = False
    display_brfc = False
    br_plot = ""
    brfc_plot = ""
    
    def get(self, request, user_id=""):
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

class FriendBiorhythm(View):
    # temp fields
    display_br = False
    display_brfc = False
    br_plot = ""
    brfc_plot = ""
    friend_brplot = ""

    def get(self, request, user_id=""):
        # temp get method
        user = userDao().get_user_by_id(id=user_id)
        if mv.userValidate.is_valid(user):

            user_bd = datetime.strptime(user['birthday'], '%d-%m-%Y')
            hoy = datetime.today()

            # needed for ticket
            self.friend_brplot = brcalc.calcBR(user_bd, hoy)

            
            context = {
                    'user_id': user_id,
                    'user_img': user['profilePicture'],
                    'user_birthdate': user_bd.strftime('%d-%m-%Y'),
                    'today_date': hoy.strftime('%d-%m-%Y'),
                    'display_br': self.display_br,
                    'display_brfc': self.display_brfc,
                    'br_plot': self.br_plot,
                    'brfc_plot': self.brfc_plot,
                    'friendName': 'obo',
                    'friend_brplot': self.friend_brplot,
            }
            return render(request, "frontend/biorhythm/friendbr.html", context)
        else:
            raise Http404("Invalid User")

# Create your views here.
