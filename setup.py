#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name="bloom_filter",
      version="0.1",
      description="A simple bloom filters implementation",
      author="Malik Diarra",
      author_email="malik.diarra@gmail.com",
      packages=find_packages(),
      url="http://www.mbzdr.com",
      entry_points={
          'console_scripts': ['spellcheck = bloom_filter.commands:spellchecker', 'bloomfiltercheck = bloom_filter.commands:check']
      },
      license="BSD",
      classifiers=['Development Status :: 4 - Beta', ],
      install_requires=[])
