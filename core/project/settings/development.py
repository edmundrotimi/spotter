from core.project.settings import BASE_DIR, DEBUG, ENV, SECRET_KEY  # type: ignore
from core.project.settings.base import INSTALLED_APPS, MIDDLEWARE  # type: ignore

# Secrete key
SECRET_KEY = SECRET_KEY

# Allowed Host
ALLOWED_HOSTS = ENV.config('ALLOWED_HOSTS', default='127.0.0.1', cast=ENV.Csv())

# Debug
DEBUG = DEBUG

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Installed app
# Add django extension and debug toolbar
if 'django_extensions' not in INSTALLED_APPS and 'debug_toolbar' not in INSTALLED_APPS:
    INSTALLED_APPS.insert(len(INSTALLED_APPS) - 2, 'django_extensions')
    INSTALLED_APPS.insert(len(INSTALLED_APPS) - 3, 'debug_toolbar')

# Django debug middleware
if 'debug_toolbar.middleware.DebugToolbarMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(len(MIDDLEWARE) - 1, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# set internal ips
INTERNAL_IPS = ['127.0.0.1']

# Cors settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
]
