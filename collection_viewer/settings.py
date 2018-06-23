# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2012 OpenPlans
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

# Django settings for the GeoNode project.
import os
from geonode.settings import *
from kombu import Queue
#
# General Django development settings
#

SITENAME = 'collection_viewer'

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

WSGI_APPLICATION = "collection_viewer.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join('development.db'),
    },
    # vector datastore for uploads
    # 'datastore' : {
    #    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #    'NAME': '',
    #    'USER' : '',
    #    'PASSWORD' : '',
    #    'HOST' : '',
    #    'PORT' : '',
    # }
}


# Additional directories which hold static files
STATICFILES_DIRS.append(
    os.path.join(LOCAL_ROOT, "static"),
)

# Note that Django automatically includes the "templates" dir in all the
# INSTALLED_APPS, se there is no need to add maps/templates or admin/templates

# Django automatically includes the "templates" dir in all the INSTALLED_APPS.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, "templates"), os.path.join(LOCAL_ROOT, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.tz',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'account.context_processors.account',
                'geonode.context_processors.resource_urls',
                'geonode.geoserver.context_processors.geoserver_urls',
                'collection_viewer.context_processors.resource_urls',
            ],
            'debug': DEBUG,
        },
    },
]

# Location of url mappings
ROOT_URLCONF = 'collection_viewer.urls'

# Location of locale files
LOCALE_PATHS = (
    os.path.join(LOCAL_ROOT, 'locale'),
    ) + LOCALE_PATHS

INSTALLED_APPS = INSTALLED_APPS + (
    'collection_viewer.collection',
    #'geonode.contrib.mp',
    #'djmp',
    #'collection_viewer.loader'
)

# Location of url mappings
ROOT_URLCONF = 'collection_viewer.urls'

DEBUG = True
DEBUG_REACT = True

REACT_DEV_SERVER = "http://cityos-sirmmo.c9users.io:8081"

ALLOWED_HOSTS = ['*']

SITEURL = "http://localhost:8000/"

#USE_DISK_CACHE = True

#TILESET_CACHE_URL = ''

CACHE_ZOOM_START = 15
CACHE_ZOOM_STOP = 18
TILESET_CACHE_DIRECTORY = 'cache/layers'

CELERY_DISABLE_RATE_LIMITS = False
CELERY_ALWAYS_EAGER = False

CELERY_QUEUES = [
     Queue('loader', routing_key='loader')
]

AW_COPERNICUS_FTP = {
    'url': 'ftp://xxx.xxx.xxx.xxx',
    'user': '',
    'password': ''
}

AW_EMS_STYLES = {
    'p': 'coll_viewer_p',
    'l': 'coll_viewer_l',
    'a': 'coll_viewer_a'
}

AW_COLLECTIONS_DOWNLOAD_PATH = ''

AW_ZIPFILE_LOCATION = ''

AW_ZIPFILE_URL = ''

# list of folders to be excluded from download
AW_FOLDERS_EXCLUDE_FROM_DOWNLOAD = ['RASTER', '00AEM']

# list of folders to be excluded from download
AW_FILES_EXCLUDE_FROM_DOWNLOAD = ['VECTOR.zip', 'source', 'sensor_metadata_a', 'area_of_interest']

OGC_SERVER['default']['datastore'] = 'datastore'

from geonode.contrib.mp.settings import *

# Load more settings from a file called local_settings.py if it exists
try:
    from local_settings import *
except ImportError:
    pass
