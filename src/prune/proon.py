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


@click.command()
@click.argument('pid')
@click.option('--dryrun', default=False, is_flag=True, help=help_dryrun)
@click.option('--doi', default=False, is_flag=True, help=help_doi)
@click.option('--password', default=None, envvar='SUDO', help=help_password)
def main(pid: str, dryrun: bool, doi: bool, password: str):
    """
        Prunes (/pro͞on/) data package(s) from PASTA+ repository.

        \b
            PID: data package identifier (scope.identifier.revision)
    """
    try:
        package = Package(pid)
        logger.info(f"Purging {pid} from {Config.HOST}")
        package.purge(dryrun, password)
    except Exception as e:
        logger.error(e)

    return 0


if __name__ == "__main__":
    main()
