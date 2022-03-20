from asyncio.windows_events import NULL
from cProfile import Profile
from http import client
from operator import length_hint
import os
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from frontend.firebase.signup import post_users
from .firebase.firebase import init_firebase
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

init_firebase()

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

def loginView(request):
    display_forecast = False
    template = loader.get_template('frontend/login.html')
    context = {
        'display_forecast': display_forecast,
    }
    return HttpResponse(template.render(context, request))

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
            post_users(username, email, birthday, profilePicture, enc_password)
            # The / line os for directory purposes
            upload_blob(bucket_name,defprofilepic_path + '/' + profilePicture, profilePicture)
            return redirect('/')    
    pass

def biorhythmView(request, user_id =0):
    if(user_id == 0):
        raise Http404("Invalid user_id.")

    template = loader.get_template("frontend/base.html"); 
    context = {
        'display_forecast': True
    }
    return HttpResponse(template.render(context, request))

def schedulerView(request):
    pass

def eventList(request):
    pass

# Create your views here.
