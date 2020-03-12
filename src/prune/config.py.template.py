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

    HOST = "PASTA_HOST"

    # PASTA database connection
    DB_USER = "DB_USER"
    DB_PW = "SECRET_PASSWORD"
    DB_HOST = f"{HOST}:PORT"
    DB_DB = "pasta"
    DB_DRIVER = "postgres+psycopg2"


