# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.TextField()),
                ('title', models.TextField(default=None, null=True)),
                ('email', models.TextField(default=None, null=True)),
                ('phone', models.TextField(default=None, null=True)),
                ('im', models.TextField(default=None, null=True)),
                ('summary', models.TextField(default=None, null=True)),
                ('url', models.TextField(unique=True)),
                ('address', models.TextField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('skill_name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(to='basic_parser.Skills'),
        ),
    ]
