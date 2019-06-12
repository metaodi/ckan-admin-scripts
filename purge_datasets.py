import re
import json
import os
import sys

# load env
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('CKAN_API_KEY')
BASE_URL = os.getenv('CKAN_BASE_URL')

import requests
import urllib3
urllib3.disable_warnings()

for dataset in sys.stdin:
    data = {
        "id": dataset.strip()
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': API_KEY
    }
    print("Trying to purge %s..." % dataset)
    # because of internal SSL issues, we need to deactivate the SSL verification
    # please consider to enable it
    r = requests.post(
        '%s/api/3/action/dataset_purge' % (BASE_URL),
        data=json.dumps(data),
        headers=headers,
        verify=False
    )
    print(r.status_code)
    print(r.content)
    print("")

