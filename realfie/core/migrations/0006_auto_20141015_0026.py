# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_fbuser_social'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fbuser',
            old_name='sex',
            new_name='gender',
        ),
    ]
