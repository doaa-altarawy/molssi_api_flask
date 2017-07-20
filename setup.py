#! /usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="molssi_api_flask",
    version="1.0.0",
    author="Doaa Altarawy",
    description="MolSSI API interface",
    long_description=__doc__,
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==0.12.2',
        'Flask_Cors==3.0.3',
        'Flask-Jsonpify==1.5.0',
        'pymongo',
        'mongoengine',
    ],
    tests_require=['pytest', 'mongomock'],
)
