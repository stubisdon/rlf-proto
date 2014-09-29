from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from realfie.core.views import IndexView, TestSearchView, TestFriendsView, EraseResultsView

urlpatterns = patterns('',
    #(r'^$', TemplateView.as_view(template_name='fb-login.html')),
    (r'^$', TestSearchView.as_view()),
    url(r'(?P<fbid>\d+)/$', TestFriendsView.as_view(), name="test_friends"),
    url(r'(?P<fbid>\d+)/erase/$', EraseResultsView.as_view(), name="erase_results"),
)
