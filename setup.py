#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="met_moai",
    version="0.1",
    packages=find_packages(),
    dependency_links = ['https://github.com/infrae/moai/tarball/master#egg=MOAI-2.0.0beta'],
    install_requires=[
        'pyoai==2.4.4',
        'MOAI>=2.0.0beta'
    ],
    entry_points={'moai.provider': ['metadata=met_moai.mmd.provider:MetaEditProvider',
                                    'svn=met_moai.mmd.provider:SVNProvider'],
                  'moai.content':['mmd=met_moai.mmd.content:MMDContent'],
                  'moai.format':['oai_dc=moai.metadata.oaidc:OAIDC',
                                 'mmd=met_moai.mmd.format:MMDFormat',
                                 'iso=met_moai.mmd.format:ISO19115',
                                 'dif=met_moai.mmd.format:DIF']}
)
