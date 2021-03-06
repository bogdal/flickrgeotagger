#! /usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='flickrgeotagger',
    author='Adam Bogdal',
    author_email='adam@bogdal.pl',
    description="Allows you to geotag your Flickr photos using a gpx file",
    version='0.0.1',
    url='http://flickrgeotagger.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=1.6',
        'gpxpy==0.9.2',
        'pytz==2013b',
        'python-flickr>=0.3.0',
        'python-openid==2.2.5',
        'python-social-auth>=0.1.24',
        'django-sekizai==0.7',
        'django-geoip-utils==0.1.1',
        'django-dropboxchooser-field>=0.0.5',
        'dj_database_url>=0.2.2',
    ],
    entry_points={
        'console_scripts': ['flickrgeotagger = flickrgeotagger:manage']},
)
