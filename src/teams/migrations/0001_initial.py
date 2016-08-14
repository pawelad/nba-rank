# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-14 14:42
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('city', models.CharField(max_length=128, verbose_name='city')),
                ('abbr', models.CharField(max_length=8, verbose_name='abbreviation')),
                ('TEAM_ID', models.PositiveIntegerField(unique=True, verbose_name='TEAM_ID')),
                ('TEAM_CODE', models.CharField(max_length=128, unique=True, verbose_name='TEAM_CODE')),
            ],
            options={
                'verbose_name_plural': 'teams',
                'ordering': ['name'],
                'verbose_name': 'team',
            },
        ),
    ]
