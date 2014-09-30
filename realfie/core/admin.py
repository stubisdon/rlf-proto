from django.contrib.admin import ModelAdmin, site
from realfie.core.models import FbUser, RlfUser, FbTask


class FbUserAdmin(ModelAdmin):
    pass

class RlfUserAdmin(ModelAdmin):
    pass

class FbTaskAdmin(ModelAdmin):
    pass

site.register(FbUser, FbUserAdmin)
site.register(FbTask, FbTaskAdmin)
site.register(RlfUser, RlfUserAdmin)
