from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from realfie.core.views import FetchView, SaveEmailView

urlpatterns = patterns('',
    url(r'eng/', TemplateView.as_view(template_name='index.html')),
    url(r'rus/', TemplateView.as_view(template_name='index_rus.html')),
    url(r'fetch/', FetchView.as_view(), name="fetch"),
    url(r'invite/', SaveEmailView.as_view(), name="invite"),
)
