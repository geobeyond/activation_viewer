import datetime
import os
import logging
from PIL import Image
import requests
from urlparse import urljoin
from collections import OrderedDict
from django.db import models
from django.db.models import signals
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager
from guardian.shortcuts import assign_perm, get_groups_with_perms, get_users_with_perms
from collection_viewer import settings
from geonode.layers.models import Layer
from geonode.base.models import Region
from geonode.geoserver.helpers import ogc_server_settings
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile


LAYERTYPES = settings.LAYERTYPES

logger = logging.getLogger(__name__)


class CollectionType(models.Model):
    """Collection types"""
    name = models.CharField(max_length=128)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name


class MapSetLayer(models.Model):
    """Link a mapset with a GeoNode layer adding metadata"""
    layer = models.OneToOneField(Layer)
    map_type = models.CharField(
        max_length=30, blank=True,
        null=True, choices=LAYERTYPES
    )
    title = models.CharField(max_length=256)
    version = models.CharField(max_length=5, blank=True, null=True)
    zip_name = models.CharField(max_length=256, blank=True, null=True)

    def __unicode__(self):
        return '%s %s, %s' % (self.title, self.map_type, self.version)


class MapSet(models.Model):
    """MapSet"""
    name = models.CharField(max_length=128)
    collection = models.ForeignKey('Collection')
    slug = models.SlugField()
    layers = models.ManyToManyField(MapSetLayer, blank=True, null=True)
    bbox_x0 = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    bbox_x1 = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    bbox_y0 = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    bbox_y1 = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)

    def set_bbox_from_layers(self):
        x0 = x1 = y0 = y1 = 0
        layers = self.layers.all()
        for i in range(layers.count()):
            ms_layer = layers[i]
            if i == 0:
                x0, x1, y0, y1 = ms_layer.layer.bbox_x0, ms_layer.layer.bbox_x1, ms_layer.layer.bbox_y0, ms_layer.layer.bbox_y1
            else:
                if ms_layer.layer.bbox_x0 < x0: x0 = ms_layer.layer.bbox_x0
                if ms_layer.layer.bbox_x1 > x1: x1 = ms_layer.layer.bbox_x1
                if ms_layer.layer.bbox_y0 < y0: y0 = ms_layer.layer.bbox_y0
                if ms_layer.layer.bbox_y1 > y1: y1 = ms_layer.layer.bbox_y1

        MapSet.objects.filter(id=self.id).update(bbox_x0=x0, bbox_x1=x1, bbox_y0=y0, bbox_y1=y1)

    class Meta:
        verbose_name_plural = 'Map Sets'
        permissions = (
            ('view_mappset', 'Can view map mapset'),
            ('change_mapset_permissions', 'Can change map set permissions'),
        )

    def __unicode__(self):
        return self.name


class Collection(models.Model):
    """Collection model"""

    collection_id = models.CharField(max_length=7, unique=True, primary_key=True)
    bbox_x0 = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    bbox_x1 = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    bbox_y0 = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    bbox_y1 = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    glide_number = models.CharField(max_length=20, blank=True, null=True)
    collection_type = models.ForeignKey(CollectionType)
    event_time = models.DateTimeField('Event Time', blank=True, null=True)
    collection_time = models.DateTimeField('Collection Time', blank=True, null=True)
    region = models.ForeignKey(Region, verbose_name='Affected Country', blank=True, null=True)
    thumbnail_url = models.CharField(max_length=256, blank=True, null=True)
    public = models.BooleanField()

    def __unicode__(self):
        return '%s, %s' % (self.collection_id, self.collection_type)

    class Meta:
        # custom permissions,
        # add, change and delete are standard in django-guardian
        permissions = (
            ('view_collection', 'Can view collection'),
            ('change_collection_permissions', 'Can change collection permissions'),
        )

    def set_permissions(self, perm_spec):
        """
        Sets an object's the permission levels based on the perm_spec JSON.


        the mapping looks like:
        {
            'users': {
                'AnonymousUser': ['view'],
                <username>: ['perm1','perm2','perm3'],
                <username2>: ['perm1','perm2','perm3']
                ...
            }
            'groups': [
                <groupname>: ['perm1','perm2','perm3'],
                <groupname2>: ['perm1','perm2','perm3'],
                ...
                ]
        }
        """

        from guardian.models import UserObjectPermission, GroupObjectPermission
        UserObjectPermission.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_pk=self.collection_id
        ).delete()
        GroupObjectPermission.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_pk=self.collection_id
        ).delete()

        if 'users' in perm_spec and "AnonymousUser" in perm_spec['users']:
            anonymous_group = Group.objects.get(name='anonymous')
            for perm in perm_spec['users']['AnonymousUser']:
                assign_perm(perm, anonymous_group, self)

        # TODO refactor code here
        if 'users' in perm_spec:
            for user, perms in perm_spec['users'].items():
                user = get_user_model().objects.get(username=user)
                for perm in perms:
                    assign_perm(perm, user, self)

        if 'groups' in perm_spec:
            for group, perms in perm_spec['groups'].items():
                group = Group.objects.get(name=group)
                for perm in perms:
                    assign_perm(perm, group, self)

    def get_all_level_info(self):

        info = {
            'users': get_users_with_perms(
                self),
            'groups': get_groups_with_perms(
                self,
                attach_perms=True)}

        return info

    def set_bbox_from_mapsets(self):
        x0 = x1 = y0 = y1 = None
        for mapset in self.mapset_set.all():
            if not x0:
                x0, x1, y0, y1 = mapset.bbox_x0, mapset.bbox_x1, mapset.bbox_y0, mapset.bbox_y1
            else:
                if mapset.bbox_x0 < x0:
                    x0 = mapset.bbox_x0
                if mapset.bbox_x1 > x1:
                    x1 = mapset.bbox_x1
                if mapset.bbox_y0 < y0:
                    y0 = mapset.bbox_y0
                if mapset.bbox_y1 > y1:
                    y1 = mapset.bbox_y1

        Collection.objects.filter(
            collection_id=self.collection_id
        ).update(bbox_x0=x0, bbox_x1=x1, bbox_y0=y0, bbox_y1=y1)

    def set_thumbnail_from_mapsets(self):
        thumbnail_name = "collection-{0}-thumb.png".format(
            self.collection_id
        )
        thumbnail_dir = os.path.join('thumbs', thumbnail_name)
        upload_path = os.path.join(settings.MEDIA_ROOT, thumbnail_dir)
        thumb = None
        coll_layers = OrderedDict()
        ms_layers = [
            MapSet.objects.filter(
                id=mapset.id
            )[0].layers.all() for mapset in self.mapset_set.all()
        ]
        for ms_layer in ms_layers:
            for i in range(ms_layer.count()):
                coll_layers.update(
                    {
                        "{0}".format(
                            os.path.basename(ms_layer[i].layer.detail_url)
                        ): "{0}".format(
                            ms_layer[i].layer.thumbnail_url
                        )
                    }
                )
        local_layers = coll_layers.keys()
        layers = ",".join(local_layers).encode('utf-8')
        params = {
            'layers': layers,
            'format': 'image/png8',
            'width': 200,
            'height': 150,
            'TIME': '-99999999999-01-01T00:00:00.0Z/99999999999-01-01T00:00:00.0Z'
        }
        p = "&".join("%s=%s" % item for item in params.items())
        thumbnail_create_url = ogc_server_settings.LOCATION + \
            "wms/reflect?" + p
        try:
            thumb = requests.get(thumbnail_create_url, stream=True)
            thumb.raw.decode_content = True
            thumb_result = Image.open(thumb.raw)

            # if storage.exists(upload_path):
            #     # Delete if exists otherwise the (FileSystemStorage)
            #     # implementation will create a new file with a unique name
            #     storage.delete(os.path.join(upload_path))

            thumb_result.save(upload_path)
        except Exception:
            logger.error(
                'Error when generating the thumbnail for resource %s.' %
                self.collection_id)
            logger.error('Check permissions for file %s.' % upload_path)

        Collection.objects.filter(
            collection_id=self.collection_id
        ).update(thumbnail_url=urljoin(
            settings.SITEURL, os.path.join(settings.MEDIA_URL, thumbnail_dir)
        ))


class CollectionMaps(models.Model):
    """
        Store information about saved maps such as layers
        order, opacity and collections
    """
    config = models.CharField(max_length=6000, null=True)
    slug = models.SlugField(default="")
    thumbnail_url = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Collection maps'

    def __unicode__(self):
        return '%s' % self.pk


class ExternalLayer(models.Model):
    """External layers related to a collection"""

    title = models.CharField(max_length=128)
    layer_name = models.CharField(max_length=128)
    url = models.URLField()
    collection = models.ForeignKey(Collection)

    def __unicode__(self):
        return self.title


def mapset_layers_changed(instance, *args, **kwargs):
    instance.set_bbox_from_layers()
    instance.collection.set_bbox_from_mapsets()
    instance.collection.set_thumbnail_from_mapsets()


signals.m2m_changed.connect(
    mapset_layers_changed, sender=MapSet.layers.through
)
