# -*- coding: utf-8 -*-
"""Check if all resources can be downloaded

Usage:
  resources_link_checker.py
  resources_link_checker.py (-h | --help)
  resources_link_checker.py --version

Options:
  -h, --help        Show this screen.
  --version         Show version.

"""

import os
import sys
import traceback
import time
from docopt import docopt
from ckanapi import RemoteCKAN
import requests
import progressbar
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
arguments = docopt(__doc__, version='Resources link checker 1.0')

try:
    BASE_URL = os.getenv('CKAN_BASE_URL')
    API_KEY = os.getenv('CKAN_API_KEY')
    ckan = RemoteCKAN(BASE_URL, apikey=API_KEY)

    # get all packages
    start = 0
    rows = 500
    packages = []
    timeout = time.time() + 60*5   # 5 minutes from now
    # run this loop max. 5min
    while time.time() < timeout:
        res = ckan.call_action('package_search', {'rows': rows, 'start': start})
        packages.extend(res['results'])
        if len(packages) >= res['count']:
            break
        start += rows
    print(f"Found {len(packages)} packages.")
    bar = progressbar.ProgressBar(max_value=len(packages), redirect_stdout=True)
    for i, pkg in enumerate(packages):
        bar.update(i+1)
        for res in pkg['resources']:
            r = requests.head(res['url'])
            if r.status_code == requests.codes.ok:
                print(f"✅ Found resource {res['id']}.")
            else:
                print(f"❌ Resource {res['id']} not found: {r.status_code} for {res['url']}!", file=sys.stderr)

except Exception as e:
    print("Error: %s" % e, file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
