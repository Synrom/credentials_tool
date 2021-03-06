#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ["dataclasses"]

test_requirements = requirements

setup(
    author="Maximilian Leiwig",
    author_email='max.leiwig@gmail.com',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="A command-line interface tool for handling credentials. Currently implements storing and comparing with a database.",
    entry_points={
        'console_scripts': [
            'credentials_tool=credentials_tool.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='credentials_tool',
    name='credentials_tool',
    packages=find_packages(include=['credentials_tool', 'credentials_tool.*']),
    data_files=[('test_data', [
        'tests/data/test_credentials1',
        'tests/data/test_credentials2',
        'tests/data/test_match'
        ])],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Synrom/credentials_tool',
    version='0.1.0',
    zip_safe=False,
)
