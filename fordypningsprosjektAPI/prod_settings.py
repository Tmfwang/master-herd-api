from fordypningsprosjektAPI.base_settings import *

# Override base.py settings here

DEBUG = False

CORS_ALLOW_ALL_ORIGINS = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True