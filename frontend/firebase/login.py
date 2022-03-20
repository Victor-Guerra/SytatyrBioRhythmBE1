from django.shortcuts import redirect
import firebase_admin
from firebase_admin import firestore
from matplotlib.style import use


def get_user_check(email, password):
    db = firestore.client()
    users = db.collection(u'Users').where(u'email', u'==', email).where(u'password', u'==', password).stream()
    for user in users:
        userMap = user.to_dict()
        userMap.update({"id":user.id})
        return userMap
        #userObject = f'{user.id} => {user.to_dict()}'
        #print(userObject)

        #if len(userObject) > 1:
         #   print("Logged in successfully")
        #else: 
         #   print("Invalid Passwords")

