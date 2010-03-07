#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages
    
import os

setup(
    name = "nginx-manager",
    version = "0.1",
    url = 'http://bitbucket.org/ehazlett/nginx-manager/wiki/Home',
	download_url = 'http://bitbucket.org/ehazlett/nginx-manager/downloads/',
    license = 'GPLv3',
    description = "Nginx Manager is a configuration management application for Nginx HTTP server.",
    author = 'Evan Hazlett',
    author_email = 'ejhazlett@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
