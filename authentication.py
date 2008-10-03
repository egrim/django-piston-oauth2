from django.http import HttpResponse
from django.contrib.auth.models import User

def django_auth(username, password):
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return user
        else:
            return False
    except User.DoesNotExist:
        return False

class HttpBasicAuthentication(object):
    def __init__(self, auth_func=django_auth, realm='Bitbucket.org API'):
        self.auth_func = auth_func
        self.realm = realm

    def is_authenticated(self, request):
        auth_string = request.META.get('HTTP_AUTHORIZATION', None)

        if not auth_string:
            return False
            
        (authmeth, auth) = auth_string.split(" ", 1)
        
        if not authmeth.lower() == 'basic':
            return False
            
        auth = auth.strip().decode('base64')
        (username, password) = auth.split(':', 1)
        
        request.user = self.auth_func(username, password)
        
        return not request.user is False
        
    def challenge(self):
        resp = HttpResponse("Authorization Required")
        resp['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        resp.status_code = 401
        return resp
        