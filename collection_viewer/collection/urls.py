from django.conf.urls import patterns, url

from django.views.generic import TemplateView


urlpatterns = patterns(
    'collection_viewer.collection.views',
    url(
        r'^$',
        TemplateView.as_view(template_name='collection_list.html'),
        name='collection_browse'
    ),
    url(r'^download/?$', 'downloadLayers', name='download_layers'),
    url(
        r'^(?P<collection_id>[^/]*)$',
        'collection_detail',
        name="collection_detail"
    ),
    url(
        r'^permissions/(?P<collection_id>\w+)$',
        'collection_permissions',
        name='collection_permissions'
    ),
)
