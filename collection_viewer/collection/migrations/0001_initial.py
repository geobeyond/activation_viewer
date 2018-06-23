# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '24_to_26'),
        ('base', '24_to_26'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('collection_id', models.CharField(max_length=7, unique=True, serialize=False, primary_key=True)),
                ('bbox_x0', models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True)),
                ('bbox_x1', models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True)),
                ('bbox_y0', models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True)),
                ('bbox_y1', models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True)),
                ('glide_number', models.CharField(max_length=20, null=True, blank=True)),
                ('event_time', models.DateTimeField(null=True, verbose_name=b'Event Time', blank=True)),
                ('collection_time', models.DateTimeField(null=True, verbose_name=b'Collection Time', blank=True)),
                ('thumbnail_url', models.CharField(max_length=256, null=True, blank=True)),
                ('public', models.BooleanField()),
            ],
            options={
                'permissions': (('view_collection', 'Can view collection'), ('change_collection_permissions', 'Can change collection permissions')),
            },
        ),
        migrations.CreateModel(
            name='CollectionMaps',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('config', models.CharField(max_length=4000, null=True)),
            ],
            options={
                'verbose_name_plural': 'Collection maps',
            },
        ),
        migrations.CreateModel(
            name='DisasterType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='ExternalLayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('layer_name', models.CharField(max_length=128)),
                ('url', models.URLField()),
                ('collection', models.ForeignKey(to='collection.Collection')),
            ],
        ),
        migrations.CreateModel(
            name='MapSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField()),
                ('bbox_x0', models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True)),
                ('bbox_x1', models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True)),
                ('bbox_y0', models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True)),
                ('bbox_y1', models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True)),
                ('collection', models.ForeignKey(to='collection.Collection')),
                ('layers', models.ManyToManyField(to='layers.Layer')),
            ],
            options={
                'verbose_name_plural': 'Map Sets',
                'permissions': (('view_mappset', 'Can view map mapset'), ('change_mapset_permissions', 'Can change map set permissions')),
            },
        ),
        migrations.AddField(
            model_name='collection',
            name='disaster_type',
            field=models.ForeignKey(to='collection.DisasterType'),
        ),
        migrations.AddField(
            model_name='collection',
            name='region',
            field=models.ForeignKey(verbose_name=b'Affected Country', blank=True, to='base.Region', null=True),
        ),
    ]
