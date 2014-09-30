from django.db import models


class FbUser(models.Model):
    fbid = models.BigIntegerField(null=True)
    name = models.CharField(max_length=80)
    photo = models.CharField(max_length=255)
    task = models.ForeignKey('FbTask', related_name='entries', null=True)

class RlfUser(models.Model):
    fbid = models.BigIntegerField(null=True)

class FbTask(models.Model):
    STATUS_CHOICES = (
        ('P', 'In progress'),
        ('OK', 'Done'),
        ('F', 'Failed'),
    )

    fbid = models.BigIntegerField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    finished = models.DateTimeField(null=True)
