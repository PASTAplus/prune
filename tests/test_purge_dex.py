#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    test_purge_dex

:Synopsis:

:Author:
    servilla

:Created:
    5/22/24
"""
import requests
import pytest


import prune.package as package


def test_purge():
    pid = "edi.9999902.1"
    code = package._purge_dex(tier="development", pid=pid, dryrun=False)
    assert code == 0
