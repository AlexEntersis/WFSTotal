# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_parser', '0002_profile_advice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='advice',
            new_name='advice_to_connect',
        ),
    ]
