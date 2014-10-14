# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import shutil

VERSION = '0.9.0'

setup(name='cloudstack.compute',
      version=VERSION,
      packages=['cloudstack','cloudstack.compute'],
      include_package_data=True,
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
            'cloudstack-api = cloudstack.compute.shell:main'
            ]
        }
      )
