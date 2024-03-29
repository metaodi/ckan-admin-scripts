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
    log.info('Copying zh_hash to hash in dataset %s...' % data['id'])
    try:
        ckan_dataset = site.call_action('package_show', data, requests_kwargs={'verify': False})
        
        for resource in ckan_dataset['resources']:
            if resource['hash']:
                log.info("Resource %s has already a hash: %s" % (resource['id'], resource['hash']))
            try:
                data = {'id': resource['id'], 'hash': resource.get('zh_hash', resource.get('hash', ''))}
                site.call_action('resource_patch', data, requests_kwargs={'verify': False})
                log.info("Set hash %s on resource %s" % (data['hash'], data['id']))
            except Exception:
                log.exception("Error occured for dataset %s, resource %s" % (data['id'], resource['id']))
                continue
    except NotFound:
        log.error('%s not found!' % data['id'])
