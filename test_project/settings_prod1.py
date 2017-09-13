DEBUG = False
ALLOWED_HOSTS = ['138.68.69.180',
                 '.voodoo-mobile.ru']


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
