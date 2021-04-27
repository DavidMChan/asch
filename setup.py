# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import pathlib

import pkg_resources
import setuptools

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

with open('README.md', 'r') as rf:
    README = rf.read()

setup(
    name='asch',
    version='1.0',
    description='Online and Web-Based Experimental Toolkit',
    long_description=README,
    long_description_content_type='text/markdown',
    author='David Chan',
    author_email='davidchan@berkeley.edu',
    url='https://github.com/DavidMChan/asch',
    license='Apache-2',
    install_requires=install_requires,
    packages=find_packages(exclude=('react')),  # exclude=('tests', 'docs'),
    entry_points={
        'console_scripts': []
    },
)
