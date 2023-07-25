import os
import json

from django.conf import settings


def configure_settings():
    """
    Configures settings for manage.py and for run_tests.py.
    """
    if not settings.configured:
        # Determine the database settings depending on if a test_db var is set in CI mode or not
        test_db = os.environ.get('DB', 'postgres')
        dbhost = os.environ.get('DBHOST', 'db')
        if test_db == 'ambition':
            db_config = {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'ambition',
                'USER': 'ambition',
                'HOST': dbhost,
            }
        elif test_db == 'postgres':
            db_config = {
                'ENGINE': 'django.db.backends.postgresql',
                'USER': 'postgres',
                'NAME': 'django_kmatch',
                'HOST': dbhost,
            }
        else:
            raise RuntimeError('Unsupported test DB {0}'.format(test_db))

        # Check env for db override (used for github actions)
        if os.environ.get('DB_SETTINGS'):
            db_config = json.loads(os.environ.get('DB_SETTINGS'))

        installed_apps = [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.admin',
            'django_kmatch',
            'django_kmatch.tests',
        ]

        settings.configure(
            SECRET_KEY='*',
            DATABASES={
                'default': db_config,
            },
            ROOT_URLCONF='django_kmatch.urls',
            INSTALLED_APPS=installed_apps,
            DEBUG=False,
            DEFAULT_AUTO_FIELD='django.db.models.AutoField',
            TEST_RUNNER='django_nose.NoseTestSuiteRunner',
            NOSE_ARGS=['--nocapture', '--nologcapture', '--verbosity=1'],
            MIDDLEWARE=(
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware'
            ),
            TEMPLATES=[{
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                        'django.template.context_processors.request',
                    ]
                }
            }],
        )
