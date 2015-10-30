# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_parser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='advice',
            field=models.TextField(null=True, default=None),
        ),
    ]
