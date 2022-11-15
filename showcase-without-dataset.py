# -*- coding: utf-8 -*-
"""Show showcases without datasets

Usage:
  showcase-without-dataset.py [--no-verify]
  showcase-without-dataset.py (-h | --help)
  showcase-without-dataset.py --version

Options:
  -h, --help                   Show this screen.
  --version                    Show version.
  --no-verify                  Option to disable SSL verification for requests.
"""

import re
import json
import os
import sys
from docopt import docopt
from ckanapi import RemoteCKAN, NotFound

# load env
from dotenv import load_dotenv
load_dotenv(verbose=True)
arguments = docopt(__doc__, version='Showcases without datasets on CKAN 1.0')

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

showcases = site.call_action('ckanext_showcase_list', requests_kwargs={'verify': verify})


for showcase in showcases:
    data = {
        "showcase_id": showcase['name']
    }
    log.info(f"Checking showcase {showcase['name']}...")
    try:
        verify = not arguments['--no-verify']
        datasets = site.call_action('ckanext_showcase_package_list', data, requests_kwargs={'verify': verify})
        print(f"Number of datasets: {datasets}")
    except NotFound:
        log.error("{data['showcase_id']} not found!")
