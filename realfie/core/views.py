from datetime import datetime
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from social.apps.django_app.default.models import UserSocialAuth
from open_facebook import OpenFacebook

from realfie.core.forms import FbidForm
from realfie.core.models import FbUser, RlfUser, FetchTask, InviteEmail
from realfie.core.tasks import fetch_fb


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        return super(IndexView, self).get_context_data(**kwargs)

class EraseResultsView(View):
    def get(self, request, *args, **kwargs):
        FbTask.objects.get(pk=kwargs['task']).delete()

        return HttpResponseRedirect('/')


class SaveEmailView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        
        if email:
            entry = InviteEmail.objects.filter(email=email).first()
            
            if not entry:
                InviteEmail(email=email).save()

        return JsonResponse({})

class FetchView(View):
    PAGE_TYPES = {
        'TV Show': 3,
        'Movie': 3,
        'Book': 4,
        'Author': 4,
    }

    def get(self, request, *args, **kwargs):
        source = request.GET.get('source')
        token = request.GET.get('access_token')
        task_id = request.GET.get('task_id')

        if task_id or source == 'facebook':
            if token:
                fb = OpenFacebook(token)
                response = fb.get('me')
                fbid = response['id']

                fbuser = FbUser.objects.filter(fbid=fbid).first()

                if not fbuser:
                    fbuser = FbUser(fbid=fbid)

                fbuser.name = response.get('name')
                try:
                    fbuser.birthday = datetime.strptime(response['birthday'], '%m/%d/%Y')
                except KeyError:
                    pass
                
                try:
                    fbuser.location_id = response['location']['id']
                    fbuser.location_name = response['location']['name']
                except KeyError:
                    pass

                fbuser.gender = response.get('gender')
                fbuser.link = response.get('link')
                fbuser.locale = response.get('locale')

                response = fb.get('me/picture', type='square', redirect='false')
                fbuser.photo = response['data']['url']

                fbuser.save()

                task = FetchTask(source='facebook', uid=fbid)
                task.save()
                fetch_fb.delay(task)

            else:
                task = FetchTask.objects.filter(pk=task_id).first()

            entries = []
            if task.status == 'completed':
                for u in task.fbusers.all():
                    if not u.likes.count():
                        continue

                    pages = []
                    
                    for p in u.likes.all():

                        pages.append({
                            'name': p.name,
                            'type': self.PAGE_TYPES.get(p.type) or 5
                        })

                    entries.append({
                        'id': u.fbid,
                        'name': u.name,
                        'photo': u.photo,
                        'sex': u.gender,
                        'edges': pages
                    })

                entries.sort(key=lambda e: len(e['edges']))
                entries.reverse()

            return JsonResponse({
                'task_id': task.pk,
                'status': task.status,
                'progress': task.progress,
                'entries': entries[:3]
            })
        
        elif source == 'instagram':
            pass


        return JsonResponse({
            'message': 'Something went wrong.',
        })
