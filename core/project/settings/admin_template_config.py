from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

from core.project.settings import ENV

# init path
path = ENV.config('ADMIN_PATH')


UNFOLD = {
    'SITE_TITLE': 'Spotter Project',
    'SITE_HEADER': 'Spotter Project',
    'SITE_URL': '/',
    # 'SITE_ICON': lambda request: static('assets/img/favicon.png'),  # both modes, optimize for 32px height
    'SITE_ICON': {
        'light': lambda request: static('assets/img/favicon.png'),  # light mode
        'dark': lambda request: static('assets/img/favicon.png'),  # dark mode
    },
    # 'SITE_LOGO': lambda request: static('logo.svg'),  # both modes, optimize for 32px height
    'SITE_LOGO': {
        'light': lambda request: static('assets/img/logo.jfif'),  # light mode
        'dark': lambda request: static('assets/img/logo.jfif'),  # dark mode
    },
    'SITE_SYMBOL': 'speed',  # symbol from icon set
    'SHOW_HISTORY': True,  # show/hide 'History' button, default: True
    'SHOW_VIEW_ON_SITE': True,  # show/hide 'View on site' button, default: True
    'ENVIRONMENT': 'core.project.settings.unfold.env.environment_callback',
    'DASHBOARD_CALLBACK': 'core.project.settings.unfold.context.dashboard_callback',
    'LOGIN': {
        'image': lambda request: static('assets/img/login-bg.jpg'),
        # 'redirect_after': lambda request: reverse_lazy('admin:APP_MODEL_changelist'),
    },
    'STYLES': [
        lambda request: static('assets/css/unfold/style.css'),
    ],
    'SCRIPTS': [
        lambda request: static('assets/js/unfold/script.js'),
    ],
    'COLORS': {
        'primary': {
            '50': '250 245 255',
            '100': '243 232 255',
            '200': '233 213 255',
            '300': '216 180 254',
            '400': '192 132 252',
            '500': '168 85 247',
            '600': '147 51 234',
            '700': '126 34 206',
            '800': '107 33 168',
            '900': '88 28 135',
            '950': '59 7 100',
        },
    },

    'SIDEBAR': {
        'show_search': True,  # Search in applications and models names
        'show_all_applications': True,  # Dropdown with all applications and models
        'navigation': [
            {
                'title': _('Navigation'),
                'separator': True,  # Top border
                'items': [
                    {
                        'title': _('Dashboard'),
                        'icon': 'dashboard',  # Supported icon set: https://fonts.google.com/icons
                        'link': lambda request: f'/{path}/',  # noqa: E501
                    },
                    {
                        'title': _('Books'),
                        'icon': 'package',
                        'link': lambda request: f'/{path}/books/book/',  # noqa: E501
                    },
                    {
                        'title': _('Authors'),
                        'icon': 'notifications',
                        'link': lambda request: f'/{path}/books/author/',  # noqa: E501
                    },
                    {
                        'title': _('Series'),
                        'icon': 'grocery',  # Supported icon set: https://fonts.google.com/icons
                        'link': lambda request: f'/{path}/works/series/',  # noqa: E501
                    },
                    {
                        'title': _('Works'),
                        'icon': 'cooking',
                        'link': lambda request: f'/{path}/works/work/',  # noqa: E501
                    },
                ],
            },
            {
                'title': _('Security'),
                'separator': True,  # Top border
                'items': [
                    {
                        'title': _('Access Attempts'),
                        'icon': 'running_with_errors',  # Supported icon set: https://fonts.google.com/icons
                        'link': lambda request: f'/{path}/defender/accessattempt/',  # noqa: E501
                    },
                ],
            },
            {
                'separator': True,  # Top border
                'items': [

                    {
                        'title': _('Users'),
                        'icon': 'badge',
                        'link': lambda request: f'/{path}/users/user/',  # noqa: E501
                    },
                    {
                        'title': _('Groups'),
                        'icon': 'groups',
                        'link': lambda request: f'/{path}/auth/group/',  # noqa: E501
                    },


                ],
            },
        ],
    },
}
