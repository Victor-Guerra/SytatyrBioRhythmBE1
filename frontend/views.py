from lib2to3.pgen2 import token
import os
import profile
from sqlite3 import Timestamp
from traceback import print_tb
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
import numpy
from rsa import encrypt
from .firebase.login import get_user_check
from django.contrib import messages
from passlib.hash import django_pbkdf2_sha256
from .firebase.firebase import userDao
from django.views import View
from . import brcalc
from . import modelvalidate as mv
from frontend.firebase.signup import post_users
from frontend.firebase.signup import post_users
from django.contrib import messages
from datetime import datetime
from django.core.files.storage import default_storage
from google.cloud import storage as gs
from pathlib import Path
from os import path
import requests
from firebase_admin import storage
import requests
from passlib.hash import django_pbkdf2_sha256
import datetime
from datetime import datetime
from datetime import timedelta
from .firebase.firebase import FirebaseAuthentication
from django.contrib.auth import login

#PATH for Google Credentials
myfilepath = Path(Path(__file__).resolve()).parent / "firebase/serviceAccountKey.json"
def_path = str(path.realpath(myfilepath))
credential_path = def_path
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

#PATH for Profile Picture Image
myprofilepic_path = Path(Path(__file__).resolve()).parent / "firebase/Img"
defprofilepic_path = str(path.realpath(myprofilepic_path))

#Bucket link to Store Files in Storage
bucket_name='biorhythmsytatyr.appspot.com'  

#REDIRECTIONS
signup_redirect = '/signup'

#Upload Files to Storage
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = gs.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def get_blob_image(picTemplate):
    storage_client = gs.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(picTemplate)
    url = blob.generate_signed_url(version="v4",expiration= 100, method="GET")
    return url


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
        email_cookie='False'
        password = request.POST['password']
        user, isvalid = get_user_check(email, password)

        if isvalid:
           #login(request,user) 
           email_cookie = email
           print("Logged in successfully")
           request.session['email'] = email_cookie
           context = {
                'user_id': user["id"],
                'email' : email_cookie,
                'user_img': get_blob_image(user['profilePicture'])
           }
           return render(request, "frontend/biorhythm/biorhythm.html", context)
           #return redirect(f'/biorhythm/{user["id"]}')
        else: 
           print("Invalid Passwords")
           context = {
                'user_id': user["id"],
                'email' : email_cookie,
           }
           messages.error(request,'Invalid Credentials, please try again')
           return render(request, "frontend/login.html", context)
           #return redirect('/')

        #user = authenticate(username=username,password = password)
        #if user is not None:
        #    auth.login(request, user)
        #    return redirect('/')
        #else:
        #    messages.info(request, 'invalid credentials')
        #    return redirect('/')

def signupView(request):

    if request.method == "GET":
        display_forecast = False
        template = loader.get_template('frontend/signup.html')
        context = {
        'display_forecast': display_forecast,
        }
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        birthday = request.POST['birthday']
        profilePicture = request.POST['profilePicture']
        password = request.POST['password']
        
        enc_password = django_pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)

        if username =="" or email =="" or birthday=="" or password=="":
            messages.error(request,'There is one or more empty fields!')
            return redirect(signup_redirect)
        else:
            try:
                datetime.strptime(birthday,"%d-%m-%Y")
            except ValueError: 
                messages.error(request,'Format of date is not correct')
                return redirect(signup_redirect)

        if len(profilePicture) > 7:
            #Creates the blob reference to file on the server
            bucket = storage.bucket(bucket_name)
            blob = bucket.blob(profilePicture)
            #Requests the file using the public url
            r = requests.head(blob.public_url)
            #Whether the file exists or not on the server
            fileExists = (r.status_code == requests.codes.ok)
            fileExists = blob.exists()

        elif profilePicture == "":
            messages.error(request,'Please upload a image')
            return redirect(signup_redirect)
        if fileExists:
             messages.error(request,'Image already exist, please change Pictures File Name')
             return redirect(signup_redirect)
        if len(username)> 1 and len(email)> 1 and len(birthday) > 1 and len(password) > 1 and len(profilePicture) > 1:
            picture = upload_blob(bucket_name,defprofilepic_path + '/' + profilePicture, profilePicture)
            post_users(username, email, birthday, picture, enc_password)
            # The / line os for directory purposes
            return redirect('/')    


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
                    'user_img': get_blob_image(user['profilePicture']),
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
