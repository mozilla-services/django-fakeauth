from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib import auth


class FakeBackend(object):
    """
    Authenticate against the settings FAKEAUTH_TOKEN.

    Use the login name you want and the token you defined in your settings.
    For example:

    FAKEAUTH_TOKEN = 'qlskdjlsqjdozaidnzalkn43'
    """

    def authenticate(self, username=None, password=None):
        if settings.FAKEAUTH_TOKEN == password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class Middleware(RemoteUserMiddleware):

    header = 'AUTHENTICATION'

    def process_request(self, request):
        #if hasattr(request, 'user') and request.user is not None:
        #    return

        user = auth.authenticate(username='tarek@mozilla.com', password='toto')
        if user:
            request.user = user
            auth.login(request, user)

        #request.session['_auth_user_id'] = 12   # 'tarek@mozilla.com'
        #request.session['_auth_user_backend'] = 'django_fakeauth.FakeBackend'
