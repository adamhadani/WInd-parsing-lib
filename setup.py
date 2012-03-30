#!/usr/bin/env python
from setuptools import setup, find_packages

import sys
import os

setup(
    name         = 'WInd-parsing-lib',
    version      = '0.1',
    description  = 'WInd parsing library',
    author       = 'Adam Ever-Hadani',
    author_email = 'adamhadani@gmail.com',
    url          = 'http://www.curbfuzz.com/',

    setup_requires = [
        "nose>=0.11",
        "coverage>=3.3.1"
        ],

    install_requires = [
        "pyyaml>=3.09",
        "BeautifulSoup>=3.2.0",
        "pyparsing>=1.5.5",
        "python-dateutil==1.5",
        "pytz"
        ],

    packages = find_packages(),
    namespace_packages = ['wind'],

    test_suite = 'nose.collector',
    
    zip_safe = True,
)
