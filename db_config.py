import os

from django.core.exceptions import ImproperlyConfigured

from dotenv import load_dotenv

load_dotenv()


def make_db(BASE_DIR=None):
    _run_mode_none_error = "You need to add 'RUN_MODE' to your '.env' file"
    _wrong_run_mode_error = "'RUN_MODE' can be only 'dev' or 'prod' but got '%(value)s'"
    run_mode = os.getenv('RUN_MODE')

    if run_mode is None:
        raise ImproperlyConfigured(_run_mode_none_error)

    if os.getenv('RUN_MODE') == 'dev':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
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
    else:
        raise ImproperlyConfigured(_wrong_run_mode_error % {"value": run_mode})

    return DATABASES
