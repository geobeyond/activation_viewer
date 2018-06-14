from django.core.urlresolvers import reverse
from tastypie.test import ResourceTestCase

from geonode.base.populate_test_data import create_models
from geonode.people.models import Profile

from .populate_test_data import create_collection_data
from .models import Collection


collection_list_url = reverse(
                            'api_dispatch_list',
                            kwargs={
                                'api_name': 'api',
                                'resource_name': 'collections'})

class CollectionTest(ResourceTestCase):
    """Collection tests"""

    fixtures = ['initial_data.json', 'bobby']

    def setUp(self):

        super(CollectionTest, self).setUp()

        create_models(type='layer')
        create_collection_data()
        self.user = 'admin'
        self.passwd = 'admin'

    def test_collection_permissions(self):
        bobby = Profile.objects.get(username='bobby')
        collection = Collection.objects.get(id=1)
        self.assertFalse(bobby.has_perm('view_collection', collection))

    def test_collections_list_get_api_non_auth(self):
        response = self.api_client.get(collection_list_url)
        self.assertValidJSONResponse(response)
        self.assertEquals(len(self.deserialize(response)['objects']), 0)

    def test_collections_list_get_api_auth(self):
        self.api_client.client.login(username=self.user, password=self.passwd)        
        response = self.api_client.get(collection_list_url)
        self.assertValidJSONResponse(response)
        self.assertEquals(len(self.deserialize(response)['objects']), 2)

    def test_collections_detail_get_api(self):
        self.api_client.client.login(username=self.user, password=self.passwd)
        response = self.api_client.get(reverse('collection_detail', 
                kwargs={'collection_id': Collection.objects.all()[0].collection_id}))
        self.assertEquals(response.status_code, 200)

    def test_collection_permission_propagates_to_its_map_products(self):
        pass
