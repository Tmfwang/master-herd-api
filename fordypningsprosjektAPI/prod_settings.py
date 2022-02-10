from fordypningsprosjektAPI.base_settings import *

# Override base.py settings here

DEBUG = False

# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000/",
    "localhost:3000/",
    "localhost:3000"
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True