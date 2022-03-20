from passlib.hash import django_pbkdf2_sha256

class User(object):
    def __init__(self, username, email, birthday, profilePicture="", password=""):
        self.username = username
        self.email = email
        self.birthday = birthday
        self.profilePicture = profilePicture
        self.password = password

    def verify_password(self,raw_password):
        return django_pbkdf2_sha256.verify(raw_password, self.password)