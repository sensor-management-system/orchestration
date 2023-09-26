# SPDX-FileCopyrightText: 2021
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

# coding: utf-8

from setuptools import find_packages, setup

NAME = "API for Sensor Management System"
VERSION = "0.0.1"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["six", "Flask", "marshmallow", "marshmallow_jsonapi", "sqlalchemy"]

setup(
    name=NAME,
    version=VERSION,
    description="RESTful API service in Python for managing sensor \
                metadata using flask-rest-jsonapi",
    author_email="",
    url="",
    keywords="web api rest jsonapi flask sqlalchemy marshmallow",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["tests"]),
)
