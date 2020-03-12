#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: setup.py

:Synopsis:

:Author:
    servilla

:Created:
    3/10/2020
"""
import setuptools

setuptools.setup(name='pastaplus.prune',
                 version='2020.03.11',
                 description='Selectively remove data packages from PASTA+',
                 author='PASTA+ project',
                 url='https://github.com/PASTAplus/prune',
                 license='Apache License, Version 2.0',
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 exclude_package_data={
                     '': ['settings.py, properties.py, config.py'],
                 }, )


def main():
    return 0


if __name__ == "__main__":
    main()
