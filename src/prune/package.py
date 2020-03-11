#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: package

:Synopsis:

:Author:
    servilla

:Created:
    3/10/20
"""
import daiquiri
import fabric
from sqlalchemy import create_engine

from prune.config import Config

logger = daiquiri.getLogger(__name__)


def get_db_connection():
    db = Config.DB_DRIVER + '://' + Config.DB_USER + ':' + Config.DB_PW + '@'\
         + Config.DB_HOST + '/' + Config.DB_DB

    connection = create_engine(db)
    return connection


def _resources(pid: str) -> list:
    c = get_db_connection()
    sql = (
        f"SELECT resource_id, resource_type, resource_location FROM "
        f"datapackagemanager.resource_registry WHERE "
        f"package_id='{pid}'"
    )
    result_set = c.execute(sql).fetchall()
    return result_set


def _purge_access_matrix(resources: list, dryrun: bool):
    c = get_db_connection()
    for resource in resources:
        resource_id = resource[0]
        sql = (
            f"DELETE FROM datapackagemanager.access_matrix WHERE "
            f"resource_id='{resource_id}'"
        )
        logger.info(sql)
        if not dryrun:
            c.execute(sql)


def _purge_resource_registry(pid: str, dryrun: bool):
    c = get_db_connection()
    sql = (
        f"DELETE FROM datapackagemanager.resource_registry WHERE "
        f"package_id='{pid}'"
    )
    logger.info(sql)
    if not dryrun:
        c.execute(sql)


def _purge_prov_matrix(pid: str, dryrun: bool):
    c = get_db_connection()
    sql = (
        f"DELETE FROM datapackagemanager.prov_matrix WHERE "
        f"derived_id='{pid}' OR source_id='{pid}'"
    )
    logger.info(sql)
    if not dryrun:
        c.execute(sql)


def _purge_journal_citation(pid: str, dryrun: bool):
    c = get_db_connection()
    sql = (
        f"DELETE FROM datapackagemanager.journal_citation WHERE "
        f"package_id ='{pid}'"
    )
    logger.info(sql)
    if not dryrun:
        c.execute(sql)


def _purge_filesystem(pid: str, location: str, dryrun: bool, password: str):
    config = fabric.Config(overrides={'sudo': {'password': password}})
    with fabric.Connection(Config.HOST, config=config, connect_timeout=15) as c:
        cmd = f"rm -rf {location}/{pid}"
        try:
            logger.info(f'{cmd}')
            if not dryrun:
                r = c.sudo(f'{cmd}')
                if r.ok:
                    logger.info(r.stdout)
        except Exception as e:
            logger.error(e)


class Package:

    def __init__(self, pid: str):
        self._pid = pid
        self._resources = _resources(self._pid)
        if len(self._resources) == 0:
            raise RuntimeError(f"{pid} not found on {Config.HOST}")
        for resource in self._resources:
            if resource[1] == 'metadata':
                self._location = resource[2]
                break

    def purge(self, dryrun: bool, password: str):
        _purge_access_matrix(self._resources, dryrun)
        _purge_resource_registry(self._pid, dryrun)
        _purge_prov_matrix(self._pid, dryrun)
        _purge_journal_citation(self._pid, dryrun)
        _purge_filesystem(self._pid, self._location, dryrun, password)

    @property
    def location(self):
        return self._location

    @property
    def resources(self):
        return self._resources

