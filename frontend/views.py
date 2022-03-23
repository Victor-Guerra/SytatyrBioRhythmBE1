import os
from sqlite3 import Timestamp
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
import numpy
from rsa import encrypt
from .firebase.login import get_user_check
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
from datetime import datetime
from datetime import timedelta
from .firebase.signup import post_users
from .firebase.users import userDao
from .firebase.firebase import init_firebase
from .firebase.friends import FriendDao
from .firebase.util import upload_blob
from .firebase.util import get_blob_image
import requests

from . import brcalc
from . import modelvalidate as mv

from cmath import pi
import enum
#import datetime
import re
import time
from unicodedata import name
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
#from .firebase.firebase import init_firebase
#from .firebase.firebase import create_user
#from .firebase.firebase import get_user
from .firebase.events import EventDAO

init_firebase()


# PATH for Google Credentials
myfilepath = settings.BASE_DIR / "frontend/firebase/serviceAccountKey.json"
def_path = str(path.realpath(myfilepath))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = def_path

# Storage Bucket
bucket_name = 'biorhythmsytatyr.appspot.com'

class LoginView(View):

    def get(self, request):
        template = loader.get_template('frontend/login.html')
        context = {
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        if email == '' or password == '':
            messages.error(request, 'Provide an email and/or a password')
            return redirect('/')
        else:
            user, isvalid = get_user_check(email, password)
        if isvalid:
            print("Logged in successfully")
            return redirect(f'/biorhythm/{user["id"]}')
        else:
            print("Invalid Passwords")
            messages.error(request, 'Invalid Credentials, please try again')
            return redirect('/')


class SignupView(View):
    signup_redirect = '/signup'

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

            if username == "" or email == "" or birthday == "" or password == "":
                messages.error(request, 'There is one or more empty fields!')
                return redirect(self.signup_redirect)
            elif profilePicture == "":
                return redirect(self.signup_redirect)
            else:
                try:
                    datetime.strptime(birthday, "%d-%m-%Y")
                except ValueError:
                    messages.error(request, 'Format of date is not correct')
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
            if err := upload_blob(bucket_name, img_path, profilePicture.name):
                messages.error(request, err)
                return redirect(self.signup_redirect)

            # Encrypt password
            enc_password = django_pbkdf2_sha256.encrypt(
                password, rounds=12000, salt_size=32)
            post_users(username, email, birthday,
                       profilePicture.name, enc_password)

            return redirect('/')

        except KeyError:
            messages.error(request, 'Please upload an image')
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
                'user_img': get_blob_image(user['profilePicture'], bucket_name),
                'modal_img': get_blob_image(user['profilePicture'], bucket_name),
                'user_birthdate': user_bd.strftime('%d-%m-%Y'),
                'today_date': hoy.strftime('%d-%m-%Y'),
                'display_br': self.display_br,
                'display_brfc': self.display_brfc,
                'br_plot': self.br_plot,
                'brfc_plot': self.brfc_plot,
                'user_name': user['username'],
            }
            return render(request, "frontend/biorhythm/biorhythm.html", context)
        else:
            raise Http404("Invalid User")


class EventList(View):

    def get(self, request, user_id=""):
        events = EventDAO().get_user_events(user_id=user_id)
        for event in events:
            date1 = datetime.fromtimestamp(int(event.get('date')))
            event.update({'date': date1.strftime("%B %d, %Y, %I:%M %p")})

        enum_events = enumerate(events)
        template = loader.get_template("frontend/events.html")
        context = {
            'user_id': user_id,
            'display_forecast': True,
            'enum_events': enum_events,
        }
        return HttpResponse(template.render(context, request))
    
    def post(self, request, user_id=""):
        delete_event = request.POST.get("delete-event")
        update_event = request.POST.get("update-event")
        add_event = request.POST.get("add-event")
        if delete_event:
            EventDAO().delete_event(event_id=delete_event)
            return redirect('/events/{0}'.format(user_id))
        if add_event:
            received_date = request.POST.get("updateDate")
            new_date = received_date
            if received_date[-4:] == "a.m.":
                new_date = received_date.replace("a.m.", "am")
            elif received_date[-4:] == "p.m.":
                new_date = received_date.replace("p.m.", "pm")
            elif received_date[-2:] == "AM":
                new_date = received_date.replace("AM", "am")
            elif received_date[-2:] == "PM":
                new_date = received_date.replace("PM", "pm")
            datetime_object = datetime.strptime(new_date, "%B %d, %Y, %I:%M %p")
            converted_date = datetime.timestamp(datetime_object)
            received_name = request.POST.get("updateName")
            received_description = request.POST.get("updateDescription")
            received_participants = request.POST.get("updateParticipants")
            separated_participants = received_participants.split(", ")
            user = userDao().get_user_by_id(user_id)
            EventDAO().create_event(event_id=update_event, date=converted_date, name=received_name,
                                    description=received_description, participants=separated_participants, user=user)
            return redirect(f'/events/{user_id}')
        if update_event:
            received_date = request.POST.get("updateDate")
            new_date = received_date
            if received_date[-4:] == "a.m.":
                new_date = received_date.replace("a.m.", "am")
            elif received_date[-4:] == "p.m.":
                new_date = received_date.replace("p.m.", "pm")
            elif received_date[-2:] == "AM":
                new_date = received_date.replace("AM", "am")
            elif received_date[-2:] == "PM":
                new_date = received_date.replace("PM", "pm")
            datetime_object = datetime.strptime(new_date, "%B %d, %Y, %I:%M %p")
            converted_date = datetime.timestamp(datetime_object)
            received_name = request.POST.get("updateName")
            received_description = request.POST.get("updateDescription")
            received_participants = request.POST.get("updateParticipants")
            separated_participants = received_participants.split(", ")
            EventDAO().update_event(event_id=update_event, date=converted_date, name=received_name,
                                    description=received_description, participants=separated_participants)
            return redirect('/events/{0}'.format(user_id))

    


class FriendList(View):
    br_graph = []
    def get(self, request, user_id=""):
        friends = userDao().get_user_friends(id=user_id)
        
        for friend in friends: 
            fuser = userDao().get_user_by_id(friend['id'])
            friend_bd = datetime.strptime(fuser['birthday'], '%d-%m-%Y')
            hoy = datetime.today()
            friend.update({"graph": brcalc.calcBR(friend_bd, hoy)})
            
        #print(self.br_graph)
        
        context = {
            'user_id': user_id,
            'friends': friends,
            #'friend_brplot': self.br_graph,
        }
        return render(request, "frontend/friends.html", context)

    def post(self, request, user_id=""):
        email = request.POST['useremail']
        user_id = request.POST['user_id']

        user = userDao().get_user_by_id(user_id)
        friend = userDao().get_user_by_email(email)

        friendao = FriendDao()
        try:
            friendao.add_new_friend(user, friend)
        except TypeError:
            messages.error(request, 'Not a valid e-mail.')
            return redirect(f'/contacts/{user_id}')
        return redirect(f'/contacts/{user_id}')
        


def updateUserDetails(request):
    userImage = request.FILES['userImage']
    userImageName = userImage.name
    userName = request.POST.get("userName")
    userBirthdate = request.POST.get("userBirthdate")
    userId = request.POST.get("userId")

    fss = FileSystemStorage()
    if not fss.exists(userImageName):
        # If the file already exists, do not save it
        file = fss.save(userImageName, userImage)

    img_path = settings.BASE_DIR / 'media/' / userImageName
    upload_blob(bucket_name, img_path, userImageName)

    userDao().update_user_details(userId, userBirthdate, userName, userImageName)
    return redirect('/biorhythm/{0}'.format(userId))
# Create your views here.
