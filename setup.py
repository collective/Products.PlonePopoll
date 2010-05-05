from setuptools import setup, find_packages
import os

version = '2.7.3b1'

setup(name='Products.PlonePopoll',
      version=version,
      description="A Poll tool for Plone 3.x",
      long_description= \
            open(os.path.join("Products", "PlonePopoll", "README.txt")).read() + 
            open(os.path.join("docs", "HISTORY.txt")).read() + 
            "\n\n",
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Zope Plone Poll',
      author='Ingeniweb',
      author_email='support@ingeniweb.com',
      url='http://ingeniweb.com',
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
