# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20141016_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='FbPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_id', models.BigIntegerField(null=True)),
                ('name', models.CharField(max_length=80, null=True)),
                ('photo', models.CharField(max_length=255, null=True)),
                ('link', models.CharField(max_length=255, null=True)),
                ('liked_by', models.ManyToManyField(related_name=b'likes', to='core.FbUser')),
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
        migrations.RemoveField(
            model_name='fbtask',
            name='user',
        ),
        migrations.DeleteModel(
            name='FbTask',
        ),
        migrations.AddField(
            model_name='fbuser',
            name='task',
            field=models.ForeignKey(related_name=b'fbusers', to='core.FetchTask', null=True),
            preserve_default=True,
        ),
    ]
