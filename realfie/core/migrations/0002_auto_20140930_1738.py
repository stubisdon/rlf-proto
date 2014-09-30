# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FbTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fbid', models.BigIntegerField(null=True)),
                ('status', models.CharField(max_length=10, null=True, choices=[(b'P', b'In progress'), (b'OK', b'Done'), (b'F', b'Failed')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='fbuser',
            name='friend_of',
        ),
        migrations.AddField(
            model_name='fbuser',
            name='task',
            field=models.ForeignKey(related_name=b'entries', to='core.FbTask', null=True),
            preserve_default=True,
        ),
    ]
