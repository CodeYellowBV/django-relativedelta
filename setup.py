#! /usr/bin/env python3

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
	README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name='django-relativedelta',
	version='1.1.1',
	package_dir={'relativedeltafield':'relativedeltafield'},
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
		'Framework :: Django :: 1.11',
		'Framework :: Django :: 2.0',
		'Framework :: Django :: 2.1',
		'Framework :: Django :: 2.2',
		'Framework :: Django :: 3.0',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Topic :: Database',
		'Topic :: Internet :: WWW/HTTP',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	],
	install_requires=[
		'Django >= 1.10, < 4.0',
		'python-dateutil >= 2.6.0',
                # Disabled (for now?) due to https://github.com/CodeYellowBV/django-relativedelta/issues/6
                # We never import it directly from the code, so that is okay
		#'psycopg2 >= 2.7.0',
	],
	tests_require=[
                # The tests do need psycopg2
		'psycopg2 >= 2.7.0',
        ],
)
