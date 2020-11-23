# -*- coding: utf-8 -*-
"""Cleanup storage directory of resources

Usage:
  cleanup_resources.py --dir <path-to-storage-dir>
  cleanup_resources.py (-h | --help)
  cleanup_resources.py --version

Options:
  -h, --help        Show this screen.
  --version         Show version.
  -d, --dir <path>  Path to the CKAN storage dir

"""

import os
import sys
import traceback
from docopt import docopt
from ckanapi import RemoteCKAN, NotFound
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
arguments = docopt(__doc__, version='Cleanup storage directory 1.0')

try:
    BASE_URL = os.getenv('CKAN_BASE_URL')
    API_KEY = os.getenv('CKAN_API_KEY')
    ckan = RemoteCKAN(BASE_URL, apikey=API_KEY)

    storage_path = arguments['--dir']

    resources_path = os.path.join(storage_path, 'resources')
    if not os.path.exists(resources_path):
        print(f"{resources_path} does not exist, make sure you passed the `storage_path` of CKAN", file=sys.stderr)
        sys.exit(1)

    for root, dirs, files in os.walk(resources_path):
        if not dirs and files:
            start = root.replace(resources_path, '').replace(os.sep, '')
            print(start)
            for f in files:
                resource_id = f"{start}{f}"
                resource_path = os.path.join(root, f)
                try:
                    ckan_resource = ckan.call_action('resource_show', {'id': resource_id})
                    print(f"✅ Found resource {resource_id}...")
                except NotFound:
                     print(f'❌ Resource {resource_id} not found!', file=sys.stderr)
                     print(f'rm {resource_path}')
                     #os.remove(resource_path)

except Exception as e:
    print("Error: %s" % e, file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
