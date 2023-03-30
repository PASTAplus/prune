# prune
Selectively prune (/pro͞on/) data packages from PASTA+

# Usage
```
Usage: prune [OPTIONS] HOST

  Prunes (/pro͞on/) data package(s) from PASTA+ repository.

  HOST: PASTA+ package server targeted for package pruning.

Options:
  --pid TEXT   Package identifier targeted for pruning (may repeat for
               multiple files)
  --file TEXT  Text file with pid(s) one per line
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
