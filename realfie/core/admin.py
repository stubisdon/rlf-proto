from django.contrib.admin import ModelAdmin, site
from realfie.core.models import FbUser, RlfUser


class FbUserAdmin(ModelAdmin):
    pass

class RlfUserAdmin(ModelAdmin):
    pass


site.register(FbUser, FbUserAdmin)
site.register(RlfUser, RlfUserAdmin)
