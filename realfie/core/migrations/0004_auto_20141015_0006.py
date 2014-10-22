# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20140930_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fbuser',
            name='task',
        ),
        migrations.AddField(
            model_name='fbuser',
            name='birthday',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fbuser',
            name='link',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fbuser',
            name='locale',
            field=models.CharField(max_length=10, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fbuser',
            name='location_id',
            field=models.BigIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fbuser',
            name='location_name',
            field=models.CharField(max_length=80, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fbuser',
            name='sex',
            field=models.CharField(max_length=10, null=True, choices=[(b'male', b'Male'), (b'female', b'Female')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fbuser',
            name='name',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='fbuser',
            name='photo',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
