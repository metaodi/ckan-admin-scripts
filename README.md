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

```bash
cat ckan_datasets_to_delete.txt | python purge_dataset.py
```
