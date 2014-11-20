from django.db import models
from social.apps.django_app.default.models import UserSocialAuth

class FbUser(models.Model):
    def __unicode__(self):
        return self.name

    SEX_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    fbid = models.BigIntegerField(null=True)
    name = models.CharField(max_length=80, null=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=SEX_CHOICES, null=True)
    photo = models.CharField(max_length=255, null=True)
    link = models.CharField(max_length=255, null=True)
    location_id = models.BigIntegerField(null=True)
    location_name = models.CharField(max_length=80, null=True)
    locale = models.CharField(max_length=10, null=True)
    task = models.ForeignKey('FetchTask', null=True, related_name='fbusers')


class IgUser(models.Model):
    def __unicode__(self):
        return self.name

    igid = models.BigIntegerField(null=True)
    name = models.CharField(max_length=80, null=True)
    photo = models.CharField(max_length=255, null=True)
    task = models.ForeignKey('FetchTask', null=True, related_name='igusers')

class FetchTask(models.Model):
    def __unicode__(self):
        return unicode(self.uid)

    STATUS_CHOICES = (
        ('started', 'Started'),
        ('ongoing', 'In progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    SOURCE_CHOICES = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
    )

    uid = models.BigIntegerField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True)
    source = models.CharField(max_length=15, choices=SOURCE_CHOICES, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    finished = models.DateTimeField(null=True)
    progress = models.DecimalField(default=0, max_digits=5, decimal_places=4)
    message = models.CharField(max_length=255, null=True)


class FbPage(models.Model):
    def __unicode__(self):
        return self.name

    page_id = models.BigIntegerField(null=True)
    name = models.CharField(max_length=80, null=True)
    type = models.CharField(max_length=80, null=True)
    photo = models.CharField(max_length=255, null=True)
    link = models.CharField(max_length=255, null=True)
    liked_by = models.ManyToManyField(FbUser, related_name='likes')

class FbAccount(models.Model):
    def __unicode__(self):
        return self.email

    email = models.EmailField(null=True)
    password = models.CharField(max_length=40, null=True)

class InviteEmail(models.Model):
    def __unicode__(self):
        return self.email

    email = models.EmailField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
