from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    #(r'^facebook/', include('django_facebook.urls')),
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^', include('realfie.core.urls')),
)
