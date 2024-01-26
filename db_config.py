import os

from dotenv import load_dotenv

load_dotenv()


def make_db(BASE_DIR=None):
    if os.getenv('RUN_MODE') == 'dev':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
        return DATABASES
    elif os.getenv('RUN_MODE') == 'prod':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': os.getenv('DB_NAME'),
                'USER': os.getenv('DB_USER'),
                'PASSWORD': os.getenv('DB_PASSWORD'),
                'HOST': 'localhost',
                'PORT': '',
            }
        }
        return DATABASES
