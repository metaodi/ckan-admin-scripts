import re
import json
import os
import sys
from ckanapi import RemoteCKAN, NotFound

# load env
from dotenv import load_dotenv
load_dotenv(verbose=True)

# setup logging
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
console = logging.StreamHandler()
logging.getLogger('').addHandler(console)
log = logging.getLogger(__name__)

BASE_URL = os.getenv('CKAN_BASE_URL')
API_KEY = os.getenv('CKAN_API_KEY')

import requests
import urllib3
urllib3.disable_warnings()

site = RemoteCKAN(BASE_URL, apikey=API_KEY)

for dataset in sys.stdin:
    data = {
        "id": dataset.strip()
    }
    log.info('Reordering %s...' % data['id'])
    try:
        ckan_dataset = site.call_action('package_show', data, requests_kwargs={'verify': False})

        resources = [{ key:value for (key,value) in r.items() if key in ['name', 'id']} for r in ckan_dataset['resources']]
        sorted_resources = sorted(resources, key=lambda r: r['name'], reverse=True) 
        sorted_ids = [r['id'] for r in sorted_resources]
        reorder = {'id': ckan_dataset['id'], 'order': sorted_ids}
        site.call_action('package_resource_reorder', reorder, requests_kwargs={'verify': False})
    except NotFound:
        log.error('%s not found!' % data['id'])
