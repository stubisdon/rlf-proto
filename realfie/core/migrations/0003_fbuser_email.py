# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_fbuser_real_fbid'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbuser',
            name='email',
            field=models.EmailField(max_length=80, null=True),
            preserve_default=True,
        ),
    ]
