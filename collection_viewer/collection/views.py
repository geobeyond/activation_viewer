import json
import operator
import StringIO

from zipfile import ZipFile

from django.core.exceptions import PermissionDenied
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db.models import Q
from django.conf import settings

from taggit.models import Tag
from guardian.shortcuts import get_perms

from geonode.security.views import _perms_info_json
from geonode.maps.models import Map

from .models import Collection, ExternalLayer, MapSetLayer, MapSet

_PERMISSION_MSG_VIEW = "You are not permitted to view this collection"

def _resolve_collection(request, collection_id, permission='collection.view_collection',
                   msg=_PERMISSION_MSG_VIEW):
    """
    Resolve the collection by the provided collection_id and check the optional permission.
    """
    collection = Collection.objects.get(collection_id=collection_id)
    if not request.user.has_perm(permission, collection):
        raise PermissionDenied(msg)

    return collection

def collection_detail(request, collection_id, template="collection_detail.html"):
    collection = _resolve_collection(request, collection_id)
    context_dict = {
        'collection': collection,
        'coll_lat': collection.bbox_y0 + abs(collection.bbox_y1 - collection.bbox_y0 )/2,
        'coll_lon': collection.bbox_x0 + abs(collection.bbox_x1 - collection.bbox_x0 )/2,
        'perms_list': get_perms(request.user, collection),
        'related_maps': Map.objects.filter(keywords__slug__in=Tag.objects.filter(name=collection.collection_id)),
        'external_layers': ExternalLayer.objects.filter(collection=collection)
    }
    return render_to_response(template, RequestContext(request, context_dict))

def collection_permissions(request, collection_id):
    collection = _resolve_collection(request, collection_id)

    if request.method == 'POST':
        permission_spec = json.loads(request.body)
        collection.set_permissions(permission_spec)

        return HttpResponse(
            json.dumps({'success': True}),
            status=200,
            content_type='text/plain'
        )

    elif request.method == 'GET':
        permission_spec = _perms_info_json(resource)
        return HttpResponse(
            json.dumps({'success': True, 'permissions': permission_spec}),
            status=200,
            content_type='text/plain'
        )
    else:
        return HttpResponse(
            'No methods other than get and post are allowed',
            status=401,
            content_type='text/plain')

def downloadLayers(request):
    if request.method == 'GET':
        query = request.GET.get('query', None)
        if query is not None:
            try:
                query = json.loads(query)
            except:
                return HttpResponse(
                    'No query object could be decoded',
                    status=400,
                    content_type='text/plain'
                )

            to_be_zipped = []
            collections = query.get('collections', [])
            if len(collections) == 0:
                return HttpResponse(
                    'Please select at least one collection',
                    status=400,
                    content_type='text/plain')

            for collection_id in collections:
                collection = Collection.objects.get(collection_id=collection_id)
                map_types = query.get('map_types', [])
                layer_names = query.get('layer_types', [])

                zip_names_filter = Q()
                if len(layer_names) > 0:
                    zip_names_filter = reduce(operator.or_, [Q(zip_name__icontains=s) for s in layer_names])

                to_be_zipped += MapSetLayer.objects.filter(
                    mapset=MapSet.objects.filter(collection=collection)).filter(
                        Q(map_type__in=map_types) | zip_names_filter
                    ).values_list('zip_name', flat=True)

            if len(to_be_zipped) == 0:
                return HttpResponse(
                    'No layers available with requested parameters',
                    status=400,
                    content_type='text/plain')

            s = StringIO.StringIO()
            with ZipFile(s, 'w') as the_zip:
                for zip_name in to_be_zipped:
                    the_zip.write('%s/%s.zip' % (settings.AW_ZIPFILE_LOCATION, zip_name),
                    '%s.zip' % zip_name)

            resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
            resp['Content-Disposition'] = 'attachment; filename=%s' % 'EMS_collections_layers.zip'
            return resp

        else:
            return HttpResponse(
                'Query parameter is missing',
                status=400,
                content_type='text/plain')
    else:
        return HttpResponse(
            'Only GET request is accepted',
            status=401,
            content_type='text/plain')
