from django.contrib.admin import ModelAdmin, site
from realfie.core.models import FbUser, FbPage, RlfUser, FetchTask


class FbUserAdmin(ModelAdmin):
    pass

class RlfUserAdmin(ModelAdmin):
    pass

class FetchTaskAdmin(ModelAdmin):
    pass

class FbPageAdmin(ModelAdmin):
    pass

site.register(FbUser, FbUserAdmin)
site.register(FetchTask, FetchTaskAdmin)
site.register(FbPage, FbPageAdmin)
site.register(RlfUser, RlfUserAdmin)
