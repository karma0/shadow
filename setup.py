#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'Jinja2>=2.9.6',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    author="Bobby",
    author_email='karma0@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A comprehensive command line utility to render templates and ease code generation.",
    entry_points={
        'console_scripts': [
            'shadow=shadow.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='shadow',
    name='shadowgen',
    packages=find_packages(include=['shadow']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/karma0/shadow',
    version='0.3.1',
    zip_safe=False,
)
