#!/usr/bin/env python

import os
import sys


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "collection_viewer.settings")
    from collection_viewer.collection.populate_test_data import create_collection_data
    create_collection_data()
