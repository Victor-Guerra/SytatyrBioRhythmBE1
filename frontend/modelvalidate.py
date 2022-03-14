from datetime import datetime

class userValidate():
    @staticmethod
    def is_valid(user):
        try:
            valid_user = {
                'username': user['username'],
                'email': user['email'],
                'birthday': user['birthday'],
                'profilePicture': user['profilePicture'],
                'password': user['password']
            }
            
            date = datetime.strptime(user['birthday'], '%d-%m-%Y')
            
            return True
        except:
            return False
