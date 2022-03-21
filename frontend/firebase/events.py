import firebase_admin
from firebase_admin import firestore

class EventDAO():
    def __init__(self):
        self.db = firestore.client()

    def get_user_events(self, user_id):
        db = self.db
        user_ref = db.collection(u'Users').document(user_id)
        user = user_ref.get().to_dict()
        user_email = user['email']
        events = db.collection(u'Events').where(u'owner.email', u'==', u"{0}".format(user_email)).stream()
        participant_events = db.collection(u'Events').where(u'participants', u'array_contains', u"{0}".format(user_email)).stream()

        eventsList = []
        for event in events:
            event_map = event.to_dict()
            event_map.update({'id': event.id})
            eventsList.append(event_map)

        for event in participant_events:
            event_map = event.to_dict()
            event_map.update({'id': event.id})
            eventsList.append(event_map)

        return eventsList

    def delete_event(self, event_id):
        db = self.db
        db.collection(u'Events').document(u"{0}".format(event_id)).delete()

    def update_event(self, event_id, date, description, name, participants):
        db = self.db
        db.collection(u'Events').document(event_id).update({'date': date, 'name': name, 'description': description, 'participants': participants})