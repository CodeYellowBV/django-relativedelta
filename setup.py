#! /usr/bin/env python3

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
	README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name='django-relativedelta',
	version='1.0.1',
	packages=find_packages(),
	include_package_data=True,
	license='MIT License',
	description='Django alternative to DurationField using dateutil.relativedelta',
	long_description=README,
	url='https://github.com/CodeYellowBV/django-relativedelta',
	author='Peter Bex',
	author_email='peter@codeyellow.nl',
	test_suite='tests',
	classifiers=[
		'Environment :: Web Environment',
		'Framework :: Django',
		'Framework :: Django :: 1.10',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Topic :: Database',
		'Topic :: Internet :: WWW/HTTP',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	],
	install_requires=[
		'Django >= 1.10',
		'python-dateutil >= 2.6.0',
		'psycopg2 >= 2.7.0',
	],
)
