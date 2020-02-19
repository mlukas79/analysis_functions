#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Setup script for python build system
'''
import os
from setuptools import setup, find_packages

from analysis_functions import about

HERE = os.path.abspath(os.path.dirname(__file__))

with open('name', 'rt') as NM:
    NAME = NM.read().strip()

setup(
    name=NAME,
    version=about.__version__,
    packages=find_packages(exclude=('functests*', 'unittests*', )),
    license=about.__license__,
    description=about.__description__,
    author=about.__author__,
    author_email=about.__author_email__,
    platforms=['windows', 'linux'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: Linux',
        'Programming Language :: Python',
    ],
    install_requires=[
        'plotly',
        'colorlover',
        'pandas',
        'jinjasql',
        'pandas'
        ],
)
