# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0002_auto_20140930_1554'),
        ('core', '0004_auto_20141015_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbuser',
            name='social',
            field=models.ForeignKey(to='default.UserSocialAuth', null=True),
            preserve_default=True,
        ),
    ]
