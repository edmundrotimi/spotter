from core.project.settings import ADMIN_PATH, ENV  # type: ignore

# General security settings in all environment
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Defender settings
DEFENDER_LOGIN_FAILURE_LIMIT = ENV.config('DEFENDER_LOGIN_FAILURE_LIMIT', cast=int)
DEFENDER_LOCK_OUT_BY_IP_AND_USERNAME = ENV.config('DEFENDER_LOCK_OUT_BY_IP_AND_USERNAME', cast=bool)
DEFENDER_COOLOFF_TIME = ENV.config('DEFENDER_COOLOFF_TIME', cast=int)
DEFENDER_LOCKOUT_TEMPLATE = ENV.config('DEFENDER_LOCKOUT_TEMPLATE')
DEFENDER_LOCKOUT_URL = ENV.config('DEFENDER_LOCKOUT_URL')
DEFENDER_USERNAME_FORM_FIELD = ENV.config('DEFENDER_USERNAME_FORM_FIELD')
DEFENDER_STORE_ACCESS_ATTEMPTS = ENV.config('DEFENDER_STORE_ACCESS_ATTEMPTS', cast=bool)
DEFENDER_ACCESS_ATTEMPT_EXPIRATION = ENV.config('DEFENDER_ACCESS_ATTEMPT_EXPIRATION', cast=int)
DEFENDER_REDIS_URL = ENV.config('DEFENDER_REDIS_URL')
DEFENDER_GET_USERNAME_FROM_REQUEST_PATH = ENV.config('DEFENDER_GET_USERNAME_FROM_REQUEST_PATH')
# DEFENDER_REVERSE_PROXY_HEADER = ENV.config('DEFENDER_REVERSE_PROXY_HEADER')
# DEFENDER_BEHIND_REVERSE_PROXY = ENV.config('DEFENDER_BEHIND_REVERSE_PROXY', cast=bool)

# CSP Settings
CSP_DEFAULT_SRC = ("'none'",)
CSP_SCRIPT_SRC = (
    "'self'",
    'https://www.google.com',
    'https://googleapis.com',
    'https://www.googletagmanager.com',
    'https://www.gstatic.com',
    'https://fonts.googleapis.com',
    'https://use.fontawesome.com',
    'https://ajax.googleapis.com',
    "'unsafe-inline'",
    'blob:',
)
CSP_CONNECT_SRC = ("'self'")
CSP_FONT_SRC = (
    "'self'",
    'https://fonts.gstatic.com',
    'https://fonts.googleapis.com',
    'https://use.fontawesome.com',
)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC_ELEM = (
    "'self'",
    'https://fonts.gstatic.com',
    'https://fonts.googleapis.com',
    'https://use.fontawesome.com',
    "'unsafe-inline'",
)

CSP_IMG_SRC = ("'self'", 'https://validator.swagger.io/', 'blob:', 'data:')
CSP_MEDIA_SRC = ("'self'",)
CSP_FORM_ACTION = ("'self'")  # Allow form submissions to URLs from the same origin
CSP_BASE_URI = ("'none'",)  # Disallow base URLs from the same origin
CSP_FRAME_ANCESTORS = ("'none'",)
# exclude admin path
CSP_EXCLUDE_URL_PREFIXES = (f'/{ADMIN_PATH}/',)
# report url
CSP_REPORT_URI = ENV.config('SENTRY_REPORT_URL')

# logout after x minutes of inactivity
AUTO_LOGOUT = {'IDLE_TIME': ENV.config('AUTO_LOGOUT_IDLE_TIME', cast=int)}
