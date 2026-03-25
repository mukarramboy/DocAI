from base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'docai'),
        'USER': os.environ.get('DB_USER', 'docai'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', '')   ,
    }
}


ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', '')]

CORS_ALLOWED_ORIGINS = [
    os.environ.get('CORS_ALLOWED_ORIGIN', '')
]
