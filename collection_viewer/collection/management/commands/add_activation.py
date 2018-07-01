from django.core.management.base import BaseCommand
from optparse import make_option

from collection_viewer.collection.models import Collection, MapProduct, CollectionType


class Command(BaseCommand):
    help = ("Ingest a new Collection into the system."
            " Map Products are added as well.")

