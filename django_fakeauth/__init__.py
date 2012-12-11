from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib import auth
import base64


class FakeAuthBackend(object):
    """
    Authenticate against the settings FAKEAUTH_TOKEN.

    Use the login name you want and the token you defined in your settings.
    For example:

    FAKEAUTH_TOKEN = 'qlskdjlsqjdozaidnzalkn43'
    """

    def authenticate(self, username=None, password=None, bypass=False):
        if settings.FAKEAUTH_TOKEN == password or bypass:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class FakeAuthMiddleware(RemoteUserMiddleware):

    def process_request(self, request):

        username, password, bypass = None, None, None

        if 'HTTP_AUTHORIZATION' in request.META:
            proto, authstr = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if proto == 'Basic':
                username, password = base64.decodestring(authstr).split(':')
        elif getattr(settings, 'FAKEAUTH_BYPASS', False):
            username = settings.FAKEAUTH_BYPASS
            bypass = True

        if username is not None:
            user = auth.authenticate(username=username, password=password,
                                     bypass=bypass)
            if user:
                request.user = user
                auth.login(request, user)
