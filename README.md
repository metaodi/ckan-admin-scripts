CKAN admin scripts
==================

A box of ckan admin scripts to make your life easier. These scripts were developed for data.stadt-zuerich.ch but might be applied to other CKAN-based open data portals as well.

## Installation

We make use of `.env` files to set environment variables, make a copy of the dist file and edit the values:

```bash
cp .env.dist .env
```

Install the dependencies (preferably in a virtualenv):

```bash
pip install -r requirements.txt
```

## Usage

The following scripts are available:

- [x] Purge datasets -> `purge_datasets.py`
- [ ] Find datasets with ugly slugs
- [ ] Find datasets with very similar slugs
- [x] Upload resources to CKAN -> `upload_resource_to_ckan.py`
- [x] Change sort-order of resources -> `order_resources.py`


The scripts are meant to be used on the command line using the help of pipes.
E.g. the script `name_to_id.py` takes a list of slugs from stdin and produces a list of correspondings IDs on stdout.
The IDs can then be used by other scripts, e.g. `purge_datasets.py`, which excepts a list of CKAN dataset IDs on stdin.

Errors are printed to stderr.

### Convert name to IDs
```bash
cat ckan_dataset_names.txt | python name_to_id.py > ckan_dataset_ids.txt # Linux/Unix
type ckan_dataset_names.txt | python name_to_id.py > ckan_dataset_ids.txt # Windows
```

### Purge
```bash
ckanapi action package_search q=tags:delete-me rows=500 -r https://data.stadt-zuerich.ch | jq -r ".results|.[]|.name" > ckan_dataset_ids.txt
cat ckan_dataset_ids.txt | python purge_dataset.py # Linux/Unix
type ckan_dataset_ids.txt | python purge_dataset.py # Windows
```
