#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os

import setuptools


# Package meta-data.
NAME = 'navigate_warehouse_via_cli'
DESCRIPTION = 'Library and slides for a presentation titled "Navigating a Data \
Warehouse via CLI"'
URL = 'https://github.com/cfournie/navigating_a_warehouse_via_cli'
EMAIL = 'chris.m.fournier@gmail.com'
AUTHOR = 'Chris Fournier'

# What packages are required for this module to be executed?
REQUIRED = [
    'pyyaml', 'faker', 'codenamize',
]

EXTRAS = {
    'dev': [
        'setuptools>=34.3',
        'pycodestyle==2.3.1',
        'pytest==3.0.6',
        'pytest-randomly==1.1.2',
        'pylint==1.7.1',
        'shopify_python==0.4.3'
    ]
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier
# for that!

HERE = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in
# file!
with io.open(os.path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = '\n' + f.read()

# Load the package's __version__.py module as a dictionary.
ABOUT = {}
with open(os.path.join(HERE, NAME, '__version__.py')) as f:
    exec(f.read(), ABOUT)  # pylint: disable=exec-used

# Where the magic happens:
setuptools.setup(
    name=NAME,
    version=ABOUT['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    py_modules=['navigate_warehouse_via_cli'],
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
