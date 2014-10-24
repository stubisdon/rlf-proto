from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from realfie.core.views import IndexView, FetchView, EraseResultsView, SaveEmailView

urlpatterns = patterns('',
    (r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'fetch/', FetchView.as_view(), name="fetch"),
    url(r'invite/', SaveEmailView.as_view(), name="invite"),
    url(r'(?P<task>\d+)/erase/$', EraseResultsView.as_view(), name="erase_results"),
)
