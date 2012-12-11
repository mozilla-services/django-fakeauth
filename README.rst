Django FakeAuth
###############

This is a fake authentication backend for django, you can use it like that (in
your settings)::

    FAKEAUTH_TOKEN = 'superkey'

    AUTHENTICATION_BACKENDS = ('django_fakeauth.FakeAuthBackend',) + AUTHENTICATION_BACKENDS
    MIDDLEWARE_CLASSES.append('access.middleware.ACLMiddleware')

    FAKEAUTH_TOKEN = os.environ.get('FAKEAUTH_TOKEN')

When doing local development, you can also ask the system to use a specific
user, like this::

    FAKEAUTH_BYPASS = 'username'
