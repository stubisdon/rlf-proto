# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20141017_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbpage',
            name='type',
            field=models.CharField(max_length=80, null=True),
            preserve_default=True,
        ),
    ]
