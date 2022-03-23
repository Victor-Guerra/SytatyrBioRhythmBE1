from django.shortcuts import redirect
import firebase_admin
from firebase_admin import firestore
from matplotlib.style import use
from passlib.hash import django_pbkdf2_sha256


def get_user_check(email,password):
    db = firestore.client()
    users = db.collection(u'Users').where(u'email', u'==', email).stream()
    for user in users:
        userMap = user.to_dict()
        userMap.update({"id":user.id})
        return (userMap,django_pbkdf2_sha256.verify(password, userMap["password"]))

