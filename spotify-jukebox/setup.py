#!/usr/bin/env python

from distutils.core import setup

setup(
    name = "SpotifyJukebox",
    version = "0.1",

    install_requires = ['flask>=0.10.1',
						'flask-login>=0.3.2',
						'flask-sqlalchemy>=2.1'
	],

    # metadata for upload to PyPI
    author = "Patrick Engelbert",
    description = "Spotify jukebox Web Server",
)