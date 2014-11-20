from django.contrib.admin import ModelAdmin, TabularInline, site
from realfie.core.models import FbUser, IgUser, FbPage, FetchTask, FbAccount, InviteEmail


class FbUserInline(TabularInline):
    model = FbUser

class FbUserAdmin(ModelAdmin):
    list_display = ['name', 'get_likes']
        
    def get_likes(self, obj):
        return ", ".join([p.name for p in obj.likes.all()])

class IgUserAdmin(ModelAdmin):
    pass

class FetchTaskAdmin(ModelAdmin):
    inlines = [
        FbUserInline,
    ]

class FbPageAdmin(ModelAdmin):
    pass

class FbAccountAdmin(ModelAdmin):
    pass

class InviteEmailAdmin(ModelAdmin):
    pass

site.register(FbUser, FbUserAdmin)
site.register(IgUser, IgUserAdmin)
site.register(FetchTask, FetchTaskAdmin)
site.register(FbPage, FbPageAdmin)
site.register(FbAccount, FbAccountAdmin)
site.register(InviteEmail, InviteEmailAdmin)
