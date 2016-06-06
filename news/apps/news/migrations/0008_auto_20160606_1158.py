# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-06 11:58
from __future__ import unicode_literals

from django.db import migrations, models


def noops(apps, schema_editor):
    pass


def move_is_publicated_into_status(apps, schema_editor):
    DRAFT = 1
    OPEN = 2

    Post = apps.get_model('news', 'Post')
    posts = Post.objects.all()

    for post in posts:
        if post.is_publicated:
            post.status = OPEN
        else:
            post.status = DRAFT
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20160509_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.IntegerField(choices=[(1, 'Kino'), (2, 'Sport'), (3, 'Technologie'), (4, 'Fotografia'), (5, 'Biznes'), (6, 'Nauka'), (7, 'Kultura'), (8, 'Polityka'), (9, 'Sztuka'), (10, 'Rozrywka'), (11, 'Inne')], default=11),
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.IntegerField(choices=[(1, 'Robocza'), (2, 'Otwarta'), (3, 'Archiwalna')], default=1),
        ),
        migrations.RunPython(move_is_publicated_into_status, noops)
    ]