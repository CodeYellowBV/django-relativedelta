#! /usr/bin/env python3

import os

from setuptools import find_packages, setup

test_deps = [
    'psycopg2-binary <= 2.8.0',
    'pytest >= 6.0.2',
    'pytest-pythonpath>=0.7.3',
    'pytest-echo>=1.7.1',
    'pytest-coverage',
    'pytest-django >= 3.7.0',
    'tox >= 3.14.3',
    'tox-pyenv >= 1.1.0',
    'bump2version >= 1.0.0',
    'flake8 >= 3.8.3',
    'isort >= 5.5.3',
    'mysqlclient >= 2.0.1'
]

setup(
    name='django-relativedelta',
    version='1.1.2',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    license='MIT License',
    description='Django alternative to DurationField using dateutil.relativedelta',
    long_description=open('README.rst').read(),
    url='https://github.com/CodeYellowBV/django-relativedelta',
    keywords='django, ',
    setup_requires=[],
    author='Code Yellow B.V.',
    author_email='django-relativedelta@codeyellow.nl',
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Django >= 1.10',
        'python-dateutil >= 2.6.0',
    ],
    tests_require=test_deps,
    extras_require={
        'test': test_deps,
    }
)
