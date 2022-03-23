from firebase_admin import firestore


class FriendDao():
    def __init__(self):
        self.db = firestore.client()

    def add_new_friend(self, user, friend):
        db = self.db
        db.collection(u'Friends').add({
            'userIds': [
                user['id'],
                friend['id']
            ],
            'users': {
                user['id']: {
                    'username': user['username'],
                    'profilePicture': user['profilePicture']
                },
                friend['id']: {
                    'username': friend['username'],
                    'profilePicture': friend['profilePicture']
                }
            }
        })
