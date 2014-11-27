# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FbAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75, null=True)),
                ('password', models.CharField(max_length=40, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FbPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_id', models.BigIntegerField(null=True)),
                ('name', models.CharField(max_length=80, null=True)),
                ('type', models.CharField(max_length=80, null=True)),
                ('photo', models.CharField(max_length=255, null=True)),
                ('link', models.CharField(max_length=255, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FbUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fbid', models.BigIntegerField(null=True)),
                ('name', models.CharField(max_length=80, null=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(max_length=10, null=True, choices=[(b'male', b'Male'), (b'female', b'Female')])),
                ('photo', models.CharField(max_length=255, null=True)),
                ('link', models.CharField(max_length=255, null=True)),
                ('location_id', models.BigIntegerField(null=True)),
                ('location_name', models.CharField(max_length=80, null=True)),
                ('locale', models.CharField(max_length=10, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FetchTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.BigIntegerField(null=True)),
                ('status', models.CharField(max_length=10, null=True, choices=[(b'started', b'Started'), (b'ongoing', b'In progress'), (b'completed', b'Completed'), (b'failed', b'Failed')])),
                ('source', models.CharField(max_length=15, null=True, choices=[(b'facebook', b'Facebook'), (b'instagram', b'Instagram')])),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('finished', models.DateTimeField(null=True)),
                ('progress', models.DecimalField(default=0, max_digits=5, decimal_places=4)),
                ('message', models.CharField(max_length=255, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IgUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('igid', models.BigIntegerField(null=True)),
                ('name', models.CharField(max_length=80, null=True)),
                ('photo', models.CharField(max_length=255, null=True)),
                ('task', models.ForeignKey(related_name=b'igusers', to='core.FetchTask', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InviteEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fbuser',
            name='task',
            field=models.ForeignKey(related_name=b'fbusers', to='core.FetchTask', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fbpage',
            name='liked_by',
            field=models.ManyToManyField(related_name=b'likes', to='core.FbUser'),
            preserve_default=True,
        ),
    ]
