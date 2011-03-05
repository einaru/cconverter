#-*- coding: utf-8 -*-
#
# Copyright (c) 2010, 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/
import os
import sys
import time
from setuptools import setup

from core import app_info
from lib.context import get_context

time_start = time.time()

CONTEXT = get_context(
            'cconverter',
            base_source=None,
            sys_prefix='',
            user=False
        )

if CONTEXT['context'] == ('windows', 'package'):
    pass

def files(*args):
    return glob.glob(os.path.join(*args))

def doc(path=''):
    return os.path.join(CONTEXT['app_doc_path'], path)

def data(path='', *paths):
    return os.path.join(CONTEXT['app_data_path'], path, *paths)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Environment :: X11 Applications',
    'Environmnet :: X11 Applications :: Gnome',
    'Ebvironment :: X11 Application :: GTK',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Topic :: Utilities',
]
packages = [
    'cconverter',
    'cconverter.core',
    'cconverter.lib',
    'cconverter.gui',
]
doc_files = [
    '']

setup(
    name = 'cconverter',
    version = app_info.version,
    author = app_info.author_name,
    author_email = app_info.author_email,
    description = app_info.description,
    license = app_info.license,
    keywords = 'currency exchange rate',
    long_description = read('README'),
    classifiers=[
        "Development Status :: 3 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPLv3"
    ],
)
