# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-27 08:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_time_record'),
    ]

    operations = [
        migrations.RenameField(
            model_name='time_record',
            old_name='student_id',
            new_name='student',
        ),
    ]
