# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_fbpage_type'),
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
    ]
