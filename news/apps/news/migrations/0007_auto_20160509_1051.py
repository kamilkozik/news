# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-09 10:51
from __future__ import unicode_literals

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20160502_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personimage',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to='person_thumbnail'),
        ),
    ]
