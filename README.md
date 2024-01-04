# prune
Selectively prune (/pro͞on/) data packages from PASTA+

# Usage
```
Usage: prune [OPTIONS] HOST

  Prunes (/pro͞on/) data package(s) from PASTA+ repository.

  HOST: PASTA+ package server targeted for package pruning.

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
  --doi        Set DOI target to tombstone (default is False)
  --sudo TEXT  SUDO password on target host (if SUDO environment variable is
               not set)
  -h, --help   Show this message and exit.
```

# Installation
1. `git clone git@github.com:PASTAplus/prune.git`
1. `cd prune`
1. `conda env create --file environment-min.yml`
1. `conda activate prune`
1. `pip install .` or `pip install --editable .`
