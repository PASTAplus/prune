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
import sys

import click
import daiquiri
import requests

from prune.config import Config
from prune.package import Package

cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/prune.log"
daiquiri.setup(
    level=logging.INFO,
    outputs=(
        daiquiri.output.File(logfile, level=logging.INFO),
        # daiquiri.output.Stream(sys.stderr, level=logging.ERROR),
    )
)

logger = daiquiri.getLogger(__name__)


def get_revisions(tier: str, pid: str) -> list:
    scope, identifier = pid.split(".")
    if tier in Config.PRODUCTION:
        url = f"https://pasta.lternet.edu/package/eml/{scope}/{identifier}"
    elif tier in Config.STAGING:
        url = f"https://pasta-s.lternet.edu/package/eml/{scope}/{identifier}"
    else:
        url = f"https://pasta-d.lternet.edu/package/eml/{scope}/{identifier}"

    r = requests.get(url=url)
    r.raise_for_status()
    revisions = r.text.split("\n")
    return revisions


help_dryrun = "Perform dry run only, do not remove any data package"
help_sudo = (
    "SUDO password for tier (if SUDO environment variable "
    "is not set) "
)
help_file = "Text file with pid(s) one per line; other options apply to each pid"
help_pid = """Package identifier targeted for pruning (may repeat for multiple data packages).
    Package identifiers with only a scope and accession identifier (e.g., edi.1) will have all
    versions of the data package pruned and the data package identifier will be locked by
    retaining the data package entry in the resource registry and setting the deactivated date."""

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("tier", required=True)
@click.option("--pid", default=None, multiple=True, help=help_pid)
@click.option("--file", default=None, help=help_file)
@click.option("--dryrun", default=False, is_flag=True, help=help_dryrun)
@click.option("--sudo", default=None, envvar="SUDO", help=help_sudo)
def main(tier: str, pid: tuple, file: str, dryrun: bool, sudo: str):
    """
        Prunes (/pro͞on/) data package(s) from PASTA repository.

        \b
        TIER: PASTA system tier targeted for package pruning.
    """

    if dryrun:
        msg = "*************************** DRYRUN ***************************"
        logger.info(msg)
        print(msg)

    if tier not in Config.PRODUCTION + Config.STAGING + Config.DEVELOPMENT:
        msg = f"Invalid tier: {tier}"
        logger.error(msg)
        print(msg)
        return 1

    if sudo is None:
        sudo = input("Enter SUDO password for host: ")

    if pid is None and file is None:
        msg = f"Usage: prune [OPTIONS] TIER\nTry 'proon.py -h' for help."
        print(msg)
        return 1
    else:
        pids = []
        if pid:
            pids = list(pid)
        if file:
            with open(file, "r") as f:
                pids += [_.strip() for _ in f]

    for pid in pids:
        try:
            if len(pid.split(".")) == 2:  # Prune entire series and lock pid
                revisions = get_revisions(tier, pid)
                for revision in revisions:
                    package = Package(tier, f"{pid}.{revision}", True, sudo, dryrun)
                    msg = f"Pruning {pid}.{revision} from {tier}"
                    logger.info(msg)
                    print(msg)
                    package.prune()
                    msg = f"Successfully pruned {pid}.{revision} from {tier}"
                    logger.info(msg)
                    print(msg)
            elif len(pid.split(".")) == 3:  # Prune single revision
                package = Package(tier, pid, False, sudo, dryrun)
                msg = f"Pruning {pid} from {tier}"
                logger.info(msg)
                print(msg)
                package.prune()
                msg = f"Successfully pruned {pid} from {tier}"
                logger.info(msg)
                print(msg)
            else:
                msg = f"Invalid pid: {pid}"
                logger.error(msg)
                print(msg)
        except Exception as e:
            logger.error(e)
            print(e)

    return 0


if __name__ == "__main__":
    main()
