# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import shutil

VERSION = '0.9.0'

setup(name='idcf.compute',
      version=VERSION,
      packages=['idcf','idcf.compute','parsedatetime'],
      include_package_data=True,
      #scripts=['scripts/idcf-compute-api'],
      install_requires=['setuptools',
                        'httplib2',
                        'simplejson',
                        'argparse',
                        'prettytable==0.5',
                        'parsedatetime==0.8.7',
                        'lxml',
                        ],
      entry_points={
        'console_scripts': [
            'idcf-compute-api = idcf.compute.shell:main'
            ]
        }
      )
