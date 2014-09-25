from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from realfie.core.forms import FbidForm
from realfie.core.models import FbUser, RlfUser
from realfie.core.tasks import test_search

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        return super(IndexView, self).get_context_data(**kwargs)

class TestSearchView(FormView):
    template_name = "test_search.html"
    form_class = FbidForm
    success_url = '/'

    def form_valid(self, form):
        fbid = form.cleaned_data['fbid']
        self.success_url = reverse("test_friends", kwargs={'fbid':fbid})

        return super(TestSearchView, self).form_valid(form)

class TestFriendsView(TemplateView):
    template_name = "test_friends.html"

    def get_context_data(self, **kwargs):
        fbid = kwargs['fbid']
        rlf_user = RlfUser.objects.filter(fbid=fbid).first()
        
        if not rlf_user:
            rlf_user = RlfUser(fbid=fbid)
            rlf_user.save()
            test_search.delay(rlf_user)

        context = super(TestFriendsView, self).get_context_data(**kwargs)
        rlf_user = RlfUser.objects.get(fbid=fbid)
        context['friends'] = FbUser.objects.filter(friend_of=rlf_user)
        context['fbid'] = fbid
        return context

class EraseResultsView(View):
    def get(self, request, *args, **kwargs):
        RlfUser.objects.get(fbid=kwargs['fbid']).delete()

        return HttpResponseRedirect('/')
