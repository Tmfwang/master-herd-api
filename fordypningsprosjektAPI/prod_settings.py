from fordypningsprosjektAPI.base_settings import *

# Override base.py settings here

DEBUG = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True