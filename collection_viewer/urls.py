from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from geonode.urls import urlpatterns, api

from collection_viewer.collection.api import CollectionResource, CollectionFullResource, CollectionTypeResource, MapSetResource, CollTagResource, CollLayerResource, CollMapResource

api.register(CollectionResource())
api.register(CollectionTypeResource())
api.register(MapSetResource())
api.register(CollTagResource())
api.register(CollLayerResource())
api.register(CollectionFullResource())
api.register(CollMapResource())


urlpatterns = patterns(
    '',
    # url(
    #     r'^/?$',
    #     TemplateView.as_view(template_name='site_base.html'), name='home'
    # ),
    url(r'^collections/viewer/?$',
        TemplateView.as_view(template_name='viewer_index.html'),
        name='viewer'),
    url(r'^collections/composer/?',
        TemplateView.as_view(template_name='map_composer.html'),
        name='composer'),
    # url(r'^maps/?',
    #    TemplateView.as_view(template_name='maps.html'),
    #    name='maps'),
    url(r'^collections/', include('collection_viewer.collection.urls')),
    url(r'', include(api.urls)),
) + urlpatterns

handler403 = 'geonode.views.err403'
