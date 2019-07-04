DEBUG = False
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db1',
        'USER': 'neformat-inc',
        'PASSWORD': 'rarara111',
        'HOST': 'localhost',
        'PORT': '',

    }
}
