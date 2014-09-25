from django.db import models


class FbUser(models.Model):
    fbid = models.BigIntegerField(null=True)
    name = models.CharField(max_length=80)
    photo = models.CharField(max_length=255)
    friend_of = models.ForeignKey('RlfUser', related_name='friends', blank=True, null=True)

class RlfUser(models.Model):
    fbid = models.BigIntegerField(null=True)
