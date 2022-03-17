import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def init_firebase():
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": "biorhythmsytatyr",
        "storageBucket": "biorhythmsytatyr.appspot.com",
        "private_key_id": "48987ae4b3fc24db8be9e1deee29888580415910",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCXyX3QlskLDSMw\nLU54YXqMCsECqFC/pAg4Cmh3aBdAc967gyhNGjRK/MvMoYId0n5FxvjZ4x/fUQTk\nL76iU/RhC3uSaGe8F7O9SA+Pakh1dchcoPcgOui+m+bXfv96HgQOkEigjXuh9IcX\nW6qR0sTtBaNZbkbK4kDfryD3pFzvDzODXGqT0RWg3AbQIUIGEe8jCFcqq17S+mY4\nuVEHGczB8i4dEiPnUQ8w0ljFxDdMc4zgo1Uacw/1fvshIIRiUbnJtHCbKHwxDGNp\n0AmeuAIG6gVGvpU3TZCGdjdqz0KfyC71GShwi2ylsGLSCRR0T05+mxfSyYmFwdqW\nhfZUfuS5AgMBAAECggEAS4oH1tDL4feaTQYnOMrOabaKYs+wTAeO3ZD0d4Ryme1w\naiJ2YpTJdI5FwKOaNUxF8mT5ALrDaGiSRhuqxG+Cve8wgub5xUaIeYlM0SNkRyyk\nV9D12/DlVsMQyatW6ofYngTZWCnBXxLqTkoc47Cgt5LoPgAfNCYQgiHOhuAiLgg+\n7XCvq4QIbNLpVp7pAUtUSngdhiIdSUwITcm8lVvU9VmOQe0u1weZlv4G6LFzkglJ\nFTpwYYVbzyieg8yqywubQUq9Hzx3gKJehZpe19ar66ETBCLkI0Gq1VGaow2V4twt\niRZVndsyPMxTjQ0TpCCsaSYSjLLJ4M39tIw6w2YqrwKBgQDI7LlMgaIpqg5KPApC\nn/doZUkY71WPt3/7y0qNhGXH1YWqOHRTkSzUMIKwodV3sBoNe39ZOj3ltAZR5gol\nteOZrdLliEwXDgqfVHXfKM0FnDYaYXt22qfR7WCgUQPyAzEeQQNaz6kKrEsH3qFQ\nhP6zdtvmJJIBK5FbQDYjA6kiqwKBgQDBZK9gdN8X+YZOJnXjMxkW29pMetApCcy3\nR1pQZ1+gvrUFD4sTerXrVjbEr4BPgdArizZMelFLG5OoC9a2pdFy16dE0TT/OGF8\n0H9Y3cm1QFBtEe6GBtvs+Fw6WPkkVPGTv67hmUu3SArthEUaQL7+eJOnaPBRWnoa\nAoMdzVI2KwKBgQCngRKJwZjbezYmlR9Io+uyUJ4792sxQR2lYLlqeXIQwuWIH0B7\nWpAw5bBOaNx5x4owq0BjtrZbhVWveUQEZDq2p78mNBabMc2RPux1eqJRhwVjwNkZ\nIPi/flIL1P6hCCAuxKxzTKP0jeaPTP7XDcj4/KIen2ZJK3UmycVYM3kRuQKBgEPu\nBdwvsR1OvGo/ADGqBSoOV4N9sBh6JLpMCeEsLl7cHeGFMCjLdZMQWXSE4OEMi/5/\ni7cZT+y95wOkBOtrG0LnlQ2LHr53I2cgJVslrHBKAvYM0mepiR6Xrm2gSwMEA0cO\nkXMU0Y+zcoMzbsJl87CW0eZ/6cnpqfHw5/VT5Yi5AoGALsxi0t/OMcQzRQcgKkzs\nKRGe58wGaHKXKt9tcbPECLFy423UOK4OO/XVkwajvuQ6Zq1QVsPbEqj9XCIKvs2e\ngpLG+D8Cpig2BQWYljR6WrX2RjzW68DvdkBpdrJpQNj7og9l0teeACeqKbmC5FqV\nOGq/WBvJss8eUtIKDO7g5/I=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-o6bcg@biorhythmsytatyr.iam.gserviceaccount.com",
        "client_id": "108866020609840584191",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-o6bcg%40biorhythmsytatyr.iam.gserviceaccount.com"
    })
    firebase_admin.initialize_app(cred)


# def create_user(user):
#     db = firestore.client()
#     # user_ref = db.collection("Users")
#     # await user_ref.add({"username": "Teston"})
#     user_ref = db.collection(u'Users')
#     user_ref.add({
#         u'username': user.username
#     })


def get_user():
    db = firestore.client()

    users = db.collection(u'Users').where(u'email', u'==', u"kike@ketriste.com").stream()

    for usr in users:
        print(f'{usr.id} => {usr.to_dict()}')

# def get_user_events():
#     db = firestore.client()

#     events = db.collection(u'Events').where(u'participants', u'array-contains', u"USER EMAIL").stream()

#     for event in events:
#         print(f'{event.id} => {event.to_dict()}')


def create_user():
    db = firestore.client()
    # user_ref = db.collection("Users")
    # await user_ref.add({"username": "Teston"})
    user_ref = db.collection(u'Users')
    user_ref.add({
        u'username': "El cenado"
    })
