from defender.models import AccessAttempt
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from core.users.utils.admin.register_defender import AttemptAdmin
from core.users.utils.admin.register_groups import UserGroupAdmin
from core.users.utils.admin.register_sites import UserSiteAdmin

from .models import User


class CustomUserAdmin(UserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ['id', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
    list_display_links = ['first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    readonly_fields = ['id', 'date_joined', 'last_login']
    search_fields = ['first_name', 'last_name', 'email']
    list_per_page = 100
    ordering = ['-date_joined']

    fieldsets = [
        [
            None,
            {
                'fields': ['email', 'password']
            },
        ],
        [
            'Personal info',
            {
                'fields': ['first_name', 'last_name']
            },
        ],
        [
            'Permissions',
            {
                'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']
            },
        ],
        [
            'Important dates',
            {
                'fields': ['last_login', 'date_joined']
            },
        ],
    ]

    add_fieldsets = [
        [
            None,
            {
                'classes': ['wide'],
                'fields': ['first_name', 'last_name', 'email', 'password1', 'password2'],
            },
        ],
    ]


# register axes in unfold template
admin.site.register(AccessAttempt, AttemptAdmin)
# register groups in unfold template
admin.site.register(Group, UserGroupAdmin)
# register sites in unfold template
admin.site.register(Site, UserSiteAdmin)

# register custom user
admin.site.register(User, CustomUserAdmin)
