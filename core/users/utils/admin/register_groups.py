from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin

# unregister and register group for unfold compatibility

# unregister all group model
admin.site.unregister(Group)


# redeclare admin and register
class UserGroupAdmin(GroupAdmin, ModelAdmin):
    pass
