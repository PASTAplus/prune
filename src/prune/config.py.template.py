#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: config.py.template

:Synopsis:

:Author:
    servilla

:Created:
    3/10/20
"""


class Config():

    # PASTA database connection
    DB_USER = "DB_USER"
    DB_PW = "SECRET_PASSWORD"
    DB_PORT = "PORT"
    DB_DB = "pasta"
    DB_DRIVER = "postgres+psycopg2"

    DATACITE_USER = "EDI.EDI"
    DATACITE_PW = "SECRET_PASSWORD"
    DATACITE_EP = "https://mds.datacite.org/doi"
    TOMBSTONE = "https://environmentaldatainitiative.org/data-package-not-available"

