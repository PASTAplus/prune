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
import logging
import os

import click
import daiquiri

from prune.package import Package

cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/prune.log"
daiquiri.setup(
    level=logging.INFO, outputs=(daiquiri.output.File(logfile), "stdout",)
)
logger = daiquiri.getLogger(__name__)

help_dryrun = "Perform dry run only, do not remove any data package"
help_doi = "Set DOI target to tombstone"
help_sudo = (
    "SUDO password on target host (if SUDO environment variable "
    "is not set) "
)
help_file = "Text file with pid(s) one per line"
help_pid = "Package identifier targeted for pruning"

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("host", required=True)
@click.option("--pid", default=None, help=help_pid)
@click.option("--file", default=None, help=help_file)
@click.option("--dryrun", default=False, is_flag=True, help=help_dryrun)
@click.option("--doi", default=False, is_flag=True, help=help_doi)
@click.option("--sudo", default=None, envvar="SUDO", help=help_sudo)
def main(host: str, pid: str, file: str, dryrun: bool, doi: bool, sudo: str):
    """
        Prunes (/pro͞on/) data package(s) from PASTA+ repository.

        \b
        HOST: PASTA+ package server targeted for package pruning.
    """
    if pid is None and file is None:
        msg = f"Usage: proon.py [OPTIONS] [PID]\nTry 'proon.py -h' for help."
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
            package = Package(host, pid, sudo, dryrun)
            logger.info(f"Pruning {pid} from {host}")
            package.purge()
            if doi:
                package.tombstone_doi()
            logger.info(f"Successfully pruned {pid} from {host}")
        except Exception as e:
            logger.error(e)

    return 0


if __name__ == "__main__":
    main()
