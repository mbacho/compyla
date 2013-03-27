#!/usr/bin/env python

from distutils.core import setup

setup(name='compyla',
      version='1.0',
      description='A compiler for the language function',
      author='erico',
      packages=['compyla', 'compyla.lexical','compyla.synt_an']
     )