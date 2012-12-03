Django FakeAuth
###############

This is a fake authentication backend for django, you can use it like that (in
your settings)::

    FAKEAUTH_TOKEN = 'superkey'

    AUTHENTICATION_BACKENDS += ('django_fakeauth.FakeBackend',)
