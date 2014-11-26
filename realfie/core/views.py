import urllib2, json, io, random
from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from social.apps.django_app.default.models import UserSocialAuth
from open_facebook import OpenFacebook

from PIL import Image, ImageOps

from realfie.core.models import FbUser, IgUser, FetchTask, InviteEmail
from realfie.core.tasks import fetch_fb, fetch_ig

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
        'Place': 1,
    }

    def get(self, request, *args, **kwargs):
        source = request.GET.get('source')
        token = request.GET.get('access_token')
        task_id = request.GET.get('task_id')
        task = None

        if task_id:
            task = FetchTask.objects.filter(pk=task_id).first()
            source = task.source

        if source == 'facebook':
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

                # FIXME
                #task = FetchTask.objects.filter(source='facebook', uid=fbid).order_by('-finished').first()
                if not task or not task.fbusers.count() > 1:
                    task = FetchTask(source='facebook', uid=fbid)
                    task.save()
                    fetch_fb.delay(task)

            entries = []
            if task.status == 'completed':
                fbuser = FbUser.objects.get(fbid=task.uid)

                for u in task.fbusers.all():
                    if not u.likes.count():
                        continue

                    pages = []
                    
                    for p in u.likes.all() & fbuser.likes.all():
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
            resp = []
            # FIXME
            #task = FetchTask.objects.filter(pk=251).first()

            #if False and token:
            if token:
                task = FetchTask(source='instagram')
                task.save()
                fetch_ig.delay(task, token)
            elif task.status == 'completed':
                iguser = task.igusers.first()

                p = {
                    'name': '',
                    'type': 5,
                }
                
                resp = [{
                    'id': iguser.igid,
                    'name': iguser.name,
                    'photo': iguser.photo,
                    'sex': 'f',
                    'edges': [p],
                }]

            return JsonResponse({
                'task_id': task.id,
                'status': task.status,
                'progress': 0,
                'entries': resp,
            })

        return JsonResponse({
            'message': 'Something went wrong.',
        })

class PostcardView(View):
    def get(self, request, *args, **kwargs):
        path = settings.STATIC_ROOT + '/www/images/pm/'
        uid = request.GET.get('fbid')
        is_ig = False

        bg_filename = 'bg-blue.png'
        paste_x = 130;
        paste_y = 120;
        if random.randint(0, 1):
            bg_filename = 'bg-red.png'
            paste_x = 260;

        if not uid:
            is_ig = True
            uid = request.GET.get('igid')

        if not is_ig:
            user = FbUser.objects.filter(fbid=uid).first()
        else:
            user = IgUser.objects.filter(igid=uid).first()

        fd = urllib2.urlopen(user.photo)
        photo_im = Image.open(io.BytesIO(fd.read()))
        bg_im = Image.open(path + bg_filename)
        mask_im = Image.open(path + 'circle-mask.png').convert('L')
        circle_im = Image.open(path + 'circle-stroke.png')

        cropped_im = photo_im.resize(mask_im.size, Image.ANTIALIAS)

        bg_im.paste(cropped_im, (paste_x, paste_y), mask_im)
        bg_im.paste(circle_im, (paste_x - 1, paste_y - 1), circle_im)

        response = HttpResponse(content_type="image/png")
        bg_im.save(response, "PNG")
        return response
