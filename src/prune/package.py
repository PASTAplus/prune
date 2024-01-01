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
import time
import urllib.parse

import daiquiri
import fabric
import requests
from sqlalchemy import create_engine

from prune.config import Config

logger = daiquiri.getLogger(__name__)


def _get_db_connection(host: str):
    db = (
        Config.DB_DRIVER
        + "://"
        + Config.DB_USER
        + ":"
        + urllib.parse.quote_plus(Config.DB_PW)
        + "@"
        + host
        + ":"
        + Config.DB_PORT
        + "/"
        + Config.DB_DB
    )

    connection = create_engine(db)
    return connection


def _resources(db_conn, pid: str) -> list:
    sql = (
        f"SELECT resource_id, resource_type, resource_location, doi FROM "
        f"datapackagemanager.resource_registry WHERE "
        f"package_id='{pid}'"
    )
    result_set = db_conn.execute(sql).fetchall()
    return result_set


def _purge_access_matrix(db_conn, resources: list, dryrun: bool):
    for resource in resources:
        resource_id = resource[0]
        sql = (
            f"DELETE FROM datapackagemanager.access_matrix WHERE "
            f"resource_id='{resource_id}'"
        )
        if not dryrun:
            logger.info(sql)
            db_conn.execute(sql)
        else:
            logger.info(f"DRYRUN: {sql}")


def _purge_reservation(db_conn, pid: str, dryrun: bool):
    scope, identifier, revision = pid.split(".")

    sql = (
        f"DELETE FROM datapackagemanager.reservation WHERE "
        f"scope = '{scope}' AND identifier = '{identifier}'"
    )
    if not dryrun:
        logger.info(sql)
        db_conn.execute(sql)
    else:
        logger.info(f"DRYRUN: {sql}")


def _purge_resource_registry(db_conn, pid: str, dryrun: bool):
    sql = (
        f"DELETE FROM datapackagemanager.resource_registry WHERE "
        f"package_id='{pid}'"
    )
    if not dryrun:
        logger.info(sql)
        db_conn.execute(sql)
    else:
        logger.info(f"DRYRUN: {sql}")


def _purge_prov_matrix(db_conn, pid: str, dryrun: bool):
    sql = (
        f"DELETE FROM datapackagemanager.prov_matrix WHERE "
        f"derived_id='{pid}' OR source_id='{pid}'"
    )
    if not dryrun:
        logger.info(sql)
        db_conn.execute(sql)
    else:
        logger.info(f"DRYRUN: {sql}")


def _purge_journal_citation(db_conn, pid: str, dryrun: bool):
    sql = (
        f"DELETE FROM datapackagemanager.journal_citation WHERE "
        f"package_id ='{pid}'"
    )
    if not dryrun:
        logger.info(sql)
        db_conn.execute(sql)
    else:
        logger.info(f"DRYRUN: {sql}")


def _purge_filesystem(
    host: str, pid: str, location: dict, dryrun: bool, password: str
):
    config = fabric.Config(overrides={"sudo": {"password": password}})
    for retry in range(0, 3):
        with fabric.Connection(host, config=config, connect_timeout=60) as c:
            cmd = f"rm -rf {location}/{pid}"
            if not dryrun:
                logger.info(f"{cmd}")
                r = c.sudo(f"{cmd}")
                if r.ok:
                    logger.info(r.stdout)
                    break
                else:
                    time.sleep(30)
            else:
                logger.info(f"DRYRUN: {cmd}")
                break


def _purge_solr(host: str, pid: str, dryrun: bool):

    scope, identifier, revision = pid.split(".")

    if "package-d" in host:
        solr_host = "solr-d"
    elif "package-s" in host:
        solr_host = "solr-s"
    else:
        solr_host = "solr"

    url = f"http://{solr_host}.lternet.edu:8983/solr/collection1/update?commit=true"
    headers = {"Content-type": "text/xml"}
    data = f"<delete><id>{scope}.{identifier}</id></delete>"

    if not dryrun:
        r = requests.post(url=url, headers=headers, data=data)
        if r.status_code != requests.codes.ok:
            logger.error(r.reason)
        else:
            logger.info(f"{url} {headers} {data}")
    else:
        logger.info(f"{url} {headers} {data}")


def _tombstone_doi(host: str, doi: str, pid: str, dryrun: bool):

    if host == Config.PRODUCTION:
        datacite_url = Config.DATACITE_EP
        datacite_user = Config.DATACITE_USER
    else:
        datacite_url = Config.DATACITE_TEST_EP
        datacite_user = Config.DATACITE_TEST_USER

    rbody = f"doi={doi}\n" + f"url={Config.TOMBSTONE}?pid={pid}&doi={doi}\n"
    if not dryrun:

        # Update DOI URL to tombstone page
        r = requests.put(
            url=datacite_url + f"doi/{doi}",
            auth=(datacite_user, Config.DATACITE_PW),
            data=rbody.encode("utf-8"),
            headers={"Content-Type": "text/plain;charset=UTF-8"},
        )
        if r.status_code != requests.codes.created:
            msg = f"Updating the DOI URL for {doi} failed: {r.reason}"
            logger.error(msg)

        # Set DOI metadata status to registered, but not searchable
        r = requests.delete(
            url=datacite_url + f"/metadata/{doi}",
            auth=(datacite_user, Config.DATACITE_PW),
            headers={"Content-Type": "text/plain;charset=UTF-8"},
        )
        if r.status_code != requests.codes.ok:
            msg = f"Updating the status for {doi} failed: {r.reason}"
            logger.error(msg)

    else:
        msg = f"DRYRUN: tombstoning {doi}\n{rbody}"
        logger.info(msg)


class Package:
    def __init__(self, host: str, pid: str, sudo: str, dryrun: bool):
        self._host = host
        self._pid = pid
        self._sudo = sudo
        self._dryrun = dryrun
        self._db_conn = _get_db_connection(self._host)
        self._resources = _resources(self._db_conn, self._pid)
        if len(self._resources) == 0:
            raise RuntimeError(f"{self._pid} not found on {self._host}")
        self._locations = dict()
        for resource in self._resources:
            if resource[1] == "metadata":
                self._locations["metadata"] = resource[2]
            if resource[1] == "data":
                self._locations["data"] = resource[2]
            if resource[1] == "dataPackage":
                self._doi = resource[3]

    def purge(self):
        try:
            # Metadata and data may be stored in different locations
            _purge_package(
                self._host,
                self._pid,
                self._locations["metadata"],
                self._dryrun,
                self._sudo,
            )
            if self._locations["metadata"] != self._locations["data"]:
                _purge_package(
                    self._host,
                    self._pid,
                    self._locations["metadata"],
                    self._dryrun,
                    self._sudo,
                )

            _purge_access_matrix(self._db_conn, self._resources, self._dryrun)
            _purge_reservation(self._db_conn, self._pid, self._dryrun)
            _purge_resource_registry(self._db_conn, self._pid, self._dryrun)
            _purge_prov_matrix(self._db_conn, self._pid, self._dryrun)
            _purge_journal_citation(self._db_conn, self._pid, self._dryrun)
            _purge_solr(self._host, self._pid, self._dryrun)
        except Exception as e:
            logger.error(e)

    def tombstone_doi(self):
        if self._doi is not None:
            _tombstone_doi(self._host, self._doi.replace("doi:", ""), self._pid, self._dryrun)
        else:
            logger.info(f"DOI for {self._pid} is None")
