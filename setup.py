#! usr/bin/env python3
from setuptools import setup

setup(name='swn_database',
    version='0.1',
    description='Database for managing SWN resources',
    author='Rob Thomas',
    packages=['swn_database'],
    install_requires=[
    ],
    tests_require=[
        'pytest',
        'pytest-cov'],  
    zip_safe=False)