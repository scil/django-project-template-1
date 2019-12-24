from .base import *

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

INTERNAL_IPS = [
    '127.0.0.1',
    '192.168.1.108',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
