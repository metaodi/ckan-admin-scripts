import re
import json
import os
import sys
from ckanapi import RemoteCKAN, NotFound

# load env
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('CKAN_BASE_URL')

import requests
import urllib3
urllib3.disable_warnings()

site = RemoteCKAN(BASE_URL)

for dataset in sys.stdin:
    data = {
        "id": dataset.strip()
    }
    try:
        ckan_dataset = site.call_action('package_show', data, requests_kwargs={'verify': False})
        print(ckan_dataset['id'])
    except NotFound:
        print('%s not found!' % data['id'], file=sys.stderr)
