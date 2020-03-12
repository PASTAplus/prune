#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: proon

:Synopsis:
    Prunes (/pro͞on/) data package(s) from PASTA+ repository.

:Author:
    servilla

:Created:
    3/10/20
"""
import click
import daiquiri

import logging
import os

from prune.config import Config
from prune.package import Package


cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/prune.log"
daiquiri.setup(level=logging.INFO,
               outputs=(daiquiri.output.File(logfile), "stdout",))
logger = daiquiri.getLogger(__name__)


help_dryrun = 'Perform dry run only, do not remove any data package'
help_doi = 'Set DOI target to tombstone'
help_password = 'SUDO password on target host (if SUDO environment variable ' \
                'is not set) '
help_file = 'Text file with pid(s) one per line'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('pid', required=False)
@click.option('--file', default=None, help=help_file)
@click.option('--dryrun', default=False, is_flag=True, help=help_dryrun)
@click.option('--doi', default=False, is_flag=True, help=help_doi)
@click.option('--password', default=None, envvar='SUDO', help=help_password)
def main(pid: str, file: str, dryrun: bool, doi: bool, password: str):
    """
        Prunes (/pro͞on/) data package(s) from PASTA+ repository.

        \b
            PID: data package identifier (scope.identifier.revision)
    """
    if pid is None and file is None:
        msg = f"Usage: proon.py [OPTIONS] [PID]\n" \
              f"Try \"proon.py -h\" for help."
        print(msg)
        return 1
    else:
        pids = []
        if pid:
            pids.append(pid)
        if file:
            with open(file, "r") as f:
                pids += [_.strip() for _ in f]

    for pid in pids:
        try:
            package = Package(pid)
            logger.info(f"Pruning {pid} from {Config.HOST}")
            package.purge(dryrun, password)
            logger.info(f"Successfully pruned {pid} from {Config.HOST}")
        except Exception as e:
            logger.error(e)

    return 0


if __name__ == "__main__":
    main()
