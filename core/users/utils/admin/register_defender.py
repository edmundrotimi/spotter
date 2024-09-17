from defender.admin import AccessAttemptAdmin
from defender.models import AccessAttempt
from django.contrib import admin
from unfold.admin import ModelAdmin

# unregister and register defender for unfold compatibility

# unregister all defender models
admin.site.unregister(AccessAttempt)


# redeclare admin and register
class AttemptAdmin(AccessAttemptAdmin, ModelAdmin):
    pass
