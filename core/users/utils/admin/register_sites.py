from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site
from unfold.admin import ModelAdmin

# unregister and register site for unfold compatibility

# unregister all site model
admin.site.unregister(Site)


# redeclare admin and register
class UserSiteAdmin(SiteAdmin, ModelAdmin):
    pass
