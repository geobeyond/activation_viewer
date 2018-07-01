# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0008_auto_20171026_0758'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DisasterType',
            new_name='CollectionType',
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='disaster_type',
            new_name='collection_type',
        ),
    ]
