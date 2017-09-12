DEBUG = False
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db2',
        'USER': 'voodoo-mobile',
        'PASSWORD': 'rarara',
        'HOST': 'localhost',
        'PORT': '',

    }
}
