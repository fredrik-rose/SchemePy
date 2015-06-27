#!/usr/bin/env python
"""
Scheme interpreter setup.
"""
from setuptools import setup


setup(name='SchemePy',
      version='1.0.0',
      description='Scheme interpreter',
      packages=['schemepy', 'schemepy.backend', 'schemepy.evalapply', 'schemepy.frontend'],
      entry_points={'console_scripts': ['schemepy = schemepy.__main__:main']},
     )
