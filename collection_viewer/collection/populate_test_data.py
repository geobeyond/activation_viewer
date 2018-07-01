from geonode.layers.models import Layer

from .models import Collection, MapProduct, CollectionType

def create_collection_data():

    collection_data = [
        {
            'collection_id': 'coll1',
            'bbox_x0': 20,
            'bbox_x1': 30,
            'bbox_y0': 20,
            'bbox_y1': 30,
            'event_time': "2015-07-17T04:23:12",
            'glide_number': "glide1",
            'collection_type': 1,
        },
        {
            'collection_id': 'coll2',
            'bbox_x0': 40,
            'bbox_x1': 40,
            'bbox_y0': 40,
            'bbox_y1': 40,
            'event_time': "2015-07-17T04:12:21",
            'glide_number': 'glide2',
            'collection_type': 1,
        }
    ]

    map_product_data = [
        {
            'name': 'mp1',
            'collection': 1,
            'layers': [1, 2],
            'type': 'reference',
            'bbox_x0': 25,
            'bbox_x1': 27,
            'bbox_y0': 25,
            'bbox_y1': 27,
        },
        {
            'name': 'mp2',
            'collection': 2,
            'layers': [3, 4],
            'type': 'grading',
            'bbox_x0': 24,
            'bbox_x1': 29,
            'bbox_y0': 24,
            'bbox_y1': 29,
        }
    ]

    firstColl = CollectionType.objects.create(
        name='FirstCollection', slug='firstcollection')
    secondColl = CollectionType.objects.create(
        name='SecondCollection', slug='secondcollection')

    for collection in collection_data:
        Collection.objects.create(collection_type=firstColl, **collection)

    for mp_data in map_product_data:
        collection = Collection.objects.get(id=mp_data['collection'])
        mp_data.pop('collection')
        layers = mp_data.pop('layers')
        mp = MapProduct.objects.create(collection=collection, **mp_data)
        for l_id in layers:
            mp.layers.add(Layer.objects.get(id=l_id))
