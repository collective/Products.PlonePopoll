# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '2.8b3'

setup(name='Products.PlonePopoll',
      version=version,
      description="A Poll tool for Plone based on archetypes.",
      long_description=open(os.path.join("README.rst")).read() +
      open(os.path.join("docs", "HISTORY.rst")).read() +
      "\n\n",
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='Zope Plone Poll',
      author='Ingeniweb',
      author_email='support@ingeniweb.com',
      url='https://github.com/collective/Products.PlonePopoll',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
