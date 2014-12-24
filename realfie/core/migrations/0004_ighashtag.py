# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_fbuser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='IgHashtag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, null=True)),
                ('liked_by', models.ManyToManyField(related_name=b'likes', to='core.IgUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
