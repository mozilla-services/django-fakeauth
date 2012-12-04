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

    def authenticate(self, username=None, password=None):
        if settings.FAKEAUTH_TOKEN == password:
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

        if 'HTTP_AUTHORIZATION' in request.META:
            authorization_header = request.META['HTTP_AUTHORIZATION']
            authstring = base64.decodestring(authorization_header.split()[1])
            username, password = authstring.split(":")

            user = auth.authenticate(username=username, password=password)
            if user:
                request.user = user
                auth.login(request, user)
