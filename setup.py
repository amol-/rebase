from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='rebase',
      version=version,
      description="A Redis based Object Model for Python",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='redis orm objects',
      author='Alessandro Molina',
      author_email='alessandro.molina@axant.it',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
