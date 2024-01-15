<p><a target="_blank" href="https://app.eraser.io/workspace/hmuPjHdhDCChbLI8okTs" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

# prune
Selectively prune (/pro͞on/) data packages from PASTA

# Usage
```
Usage: prune [OPTIONS] TIER
  Prunes (/pro͞on/) data package(s) from PASTA repository.
  TIER: PASTA system tier targeted for package pruning.
Options:
  --pid TEXT   Package identifier targeted for pruning (may repeat for
               multiple data packages). Package identifiers with only a scope
               and accession identifier (e.g., edi.1) will have all versions
               of the data package pruned and the data package identifier will
               be locked by retaining the data package entry in the resource
               registry and setting the deactivated date.
  --file TEXT  Text file with pid(s) one per line; other options apply to each
               pid
  --dryrun     Perform dry run only, do not remove any data package
  --sudo TEXT  SUDO password for tier (if SUDO environment variable is not
               set)
  -h, --help   Show this message and exit.
```
# Installation
1. `git clone git@github.com:PASTAplus/prune.git` 
2. `cd prune` 
3. `conda env create --file environment-min.yml` 
4. `conda activate prune` 
5. `pip install .`  or `pip install --editable .` 
# About Prune
Prune selectively removes data package artifacts from the PASTA data repository ecosystem, including setting a DOI tombstone page in DataCite metadata. Prune is designed to remove artifacts that have been published incorrectly or violate a [﻿DRM](https://en.wikipedia.org/wiki/Digital_rights_management) license.

Prune accepts as input a fully qualified package identifier (`scope.identifier.revision`) or only the scope and identifier to remove the entire data package series (all revisions). In this latter case, Prune locks the data package identifier series to prevent future use of the identifier.

# What artifacts does Prune touch?
Prune will remove all database and file system artifacts of the data package. The databases affected are the `datapackagemanager.resource_registry` , `datapackagemanager.access_matrix` ,  `datapackagemanager.reservation` , `datapackagemanager.prov_matrix` , and `datapackagemanager.journal_citation` . All physical files, including `Leve-0-EML.xml` , `Level-1-EML.xml` ,  `Level-1-DC.xml` , `quality_report.xml` , and data files are deleted from the file system. The search index for the data package is also removed from PASTA's "Solr" search engine. In addition, cache files or other components are removed from the following services: "cite", "seo", "ridare", and "dex." Data package metadata in DataCite will be modified to include a tombstone link and set the record to non-searchable.

![Figure 1](/.eraser/hmuPjHdhDCChbLI8okTs___fnGbXWbo0lO57yDHg7xqtdn0bvA3___---figure---LrhQylZAoyJ5l6hhBF9F4---figure---iaVoOXEgtTFIi_A2oHaa_A.png "Figure 1")




<!--- Eraser file: https://app.eraser.io/workspace/hmuPjHdhDCChbLI8okTs --->