import firebase_admin
from firebase_admin import firestore
from ..objects.user import User


def post_users(username, email, birthday, profilePicture, password):
    db= firestore.client()
    user = User(username, email, birthday, profilePicture, password)
    db.collection(u'Users').add(vars(user))
    return user



