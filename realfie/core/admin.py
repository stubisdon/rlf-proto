from django.contrib.admin import ModelAdmin, site
from realfie.core.models import FbUser, FbPage, RlfUser, FetchTask, FbAccount, InviteEmail


class FbUserAdmin(ModelAdmin):
    pass

class RlfUserAdmin(ModelAdmin):
    pass

class FetchTaskAdmin(ModelAdmin):
    pass

class FbPageAdmin(ModelAdmin):
    pass

class FbAccountAdmin(ModelAdmin):
    pass

class InviteEmailAdmin(ModelAdmin):
    pass

site.register(FbUser, FbUserAdmin)
site.register(FetchTask, FetchTaskAdmin)
site.register(FbPage, FbPageAdmin)
site.register(RlfUser, RlfUserAdmin)
site.register(FbAccount, FbAccountAdmin)
site.register(InviteEmail, InviteEmailAdmin)
