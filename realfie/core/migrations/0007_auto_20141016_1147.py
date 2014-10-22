# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20141015_0026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fbtask',
            name='fbid',
        ),
        migrations.RemoveField(
            model_name='fbuser',
            name='social',
        ),
        migrations.AddField(
            model_name='fbtask',
            name='user',
            field=models.ForeignKey(to='core.FbUser', null=True),
            preserve_default=True,
        ),
    ]
