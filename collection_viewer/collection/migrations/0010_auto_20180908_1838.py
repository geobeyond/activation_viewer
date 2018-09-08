# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0009_auto_20180701_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectionmaps',
            name='slug',
            field=models.SlugField(default=b''),
        ),
        migrations.AddField(
            model_name='collectionmaps',
            name='thumbnail_url',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
