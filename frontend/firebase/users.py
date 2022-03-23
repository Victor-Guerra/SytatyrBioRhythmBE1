from traceback import print_tb
from firebase_admin import firestore
from .util import get_blob_image


class userDao():
    def __init__(self):
        self.db = firestore.client()
        self.bucket_name = 'biorhythmsytatyr.appspot.com'

    def get_user_by_id(self, id):
        db = self.db

        user_ref = db.collection(u'Users').document(id)
        user = user_ref.get().to_dict()
        print(id)
        user.update({"id": id})
        return user
    
    def get_user_by_email(self, email):
        db = self.db

        user_ref = db.collection(u'Users').where(u'email', u'==', email).stream()
        for user in user_ref:
            user_dict = user.to_dict()
            user_dict.update({"id": user.id})
            return user_dict

    def update_user_details(self, id, user_birthdate, user_name, user_img):
        db = self.db
        
        db.collection(u'Users').document(id).update({u'birthday': user_birthdate})
        db.collection(u'Users').document(id).update({u'username': user_name})
        db.collection(u'Users').document(id).update({u'profilePicture': user_img})

    def get_user_friends(self, id):
        db = self.db
        friends_ref = db.collection(u'Friends').where(f'userIds', u'array_contains', id).stream()

        friend_list = []
        for friends in friends_ref:
            frds = friends.to_dict()
            frds = frds['users']
            del frds[id]
            for key in frds:
                name = frds[key]
                name.update({"id": key})
                name.update({"profilePicture": get_blob_image(name['profilePicture'], self.bucket_name)})
                friend_list.append(name)
        print(friend_list)
        return friend_list
    
