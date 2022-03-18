class User(object):
    def __init__(self, username, email, birthday, profilePicture="", password=""):
        self.username = username
        self.email = email
        self.birthday = birthday
        self.profilePicture = profilePicture
        self.password = password