import re
import json
import os

# load env
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('CKAN_API_KEY')
BASE_URL = os.getenv('CKAN_BASE_URL')

datasets = """eingetragene-und-aufgeloste-partnerschaften-nach-geschlecht-seit-2014
durchschnittliches-alter-bei-der-ersten-eingetragener-partnerschaft-nach-geschlecht-seit-2014
eingetragene-partnerschaften-nach-geschlecht-und-herkunft-seit-2014
todesfalle-nach-monat-stadtquartier-geschlecht-altersgruppe-und-herkunft-seit-20134
zuzuge-nach-monat-stadtquartier-geschlecht-altersgruppe-und-herkunft-seit-20132
todesfalle-nach-monat-stadtquartier-geschlecht-altersgruppe-und-herkunft-seit-20132
ubersichtsplan-20112
friedhof1
velopumpstation"""

dataset_list = datasets.splitlines()

print dataset_list
print len(dataset_list)

import requests

for dataset in dataset_list:
    data = {
        "id": dataset
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': API_KEY
    }
    print "Trying to purge %s..." % dataset
    r = requests.post(
        '%s/api/3/action/dataset_purge' % (BASE_URL),
        data=json.dumps(data),
        headers=headers
    )
    print r.status_code
    print r.content
    print ""

