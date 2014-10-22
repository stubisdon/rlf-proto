from datetime import datetime
from open_facebook import OpenFacebook
from social.apps.django_app.default.models import UserSocialAuth
from realfie.core.models import FbUser


def load_detailed_profile(strategy, details, user=None, *args, **kwargs):
    if user:
        u = UserSocialAuth.get_social_auth_for_user(user)[0]
        access_token = u.extra_data['access_token']
        response = kwargs['response']

        fbuser = FbUser.objects.filter(fbid=response['id']).first()

        if not fbuser:
            fbuser = FbUser(fbid=response['id'])

        fbuser.name = response['name']
        fbuser.birthday = datetime.strptime(response['birthday'], '%m/%d/%Y')
        fbuser.gender = response['gender']
        fbuser.link = response['link']
        fbuser.location_id = response['location']['id']
        fbuser.location_name = response['location']['name']
        fbuser.locale = response['locale']
        fbuser.social = u

        fb = OpenFacebook(response['access_token'])
        photo = fb.get('me/picture', type='square', redirect='false')
        fbuser.photo = photo['data']['url']

        fbuser.save()
