#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="met_moai",
    version="0.1",
    packages=find_packages(),
    dependency_links = ['https://github.com/infrae/moai/tarball/master#egg=MOAI-2.0.0beta'],
    install_requires=[
        'pyoai==2.4.4',
        'MOAI>=2.0.0beta',
        'svn==0.3.39'
    ],
    entry_points={'moai.provider': ['svn=met_moai.mmd.provider:SVNProvider'],
                  'moai.content':['mmd_example=met_moai.mmd.content:MMDContent'],
                  'moai.format':['oai_dc=moai.metadata.oaidc:OAIDC',
                                 'mmd=met_moai.mmd.format:MMDFormat',
                                 'iso=met_moai.mmd.format:ISO19115']}
)
