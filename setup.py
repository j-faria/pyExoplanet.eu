#!/usr/bin/env python

from setuptools import setup

setup(name='pyExoplaneteu',
      version='1.0',
      description='A pure-Python package to download data from '\
                  'the Extrasolar Planets Encyclopaedia',
      long_description=open('README.rst').read(),
      author='João Faria',
      author_email='joao.faria@astro.up.pt',
      license='MIT',
      url='https://github.com/j-faria/pyExoplanet.eu',
      packages=['pyexoplaneteu'],
      classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ),
     )