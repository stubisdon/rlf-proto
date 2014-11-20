# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_inviteemail'),
    ]

    operations = [
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
    ]
