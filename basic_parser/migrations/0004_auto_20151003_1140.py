# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_parser', '0003_auto_20150920_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(null=True, default=None, max_length=300),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.CharField(null=True, default=None, max_length=300),
        ),
        migrations.AlterField(
            model_name='profile',
            name='im',
            field=models.CharField(null=True, default=None, max_length=300),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(null=True, default=None, max_length=300),
        ),
        migrations.AlterField(
            model_name='profile',
            name='title',
            field=models.CharField(null=True, default=None, max_length=300),
        ),
        migrations.AlterField(
            model_name='skills',
            name='skill_name',
            field=models.CharField(max_length=300),
        ),
    ]
