# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20140930_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbtask',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fbtask',
            name='finished',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
