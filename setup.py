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
import glob

from distutils.core import setup

from cconverter.core import app_info

_classifiers = [
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
_packages = [
    'cconverter',
    'cconverter.core',
    'cconverter.lib',
    'cconverter.gui',
]
_data_files = [
    ('share/icons/hicolor/16x16/apps', glob.glob('data/icons/hicolor/16x16/apps/*png')),
    ('share/icons/hicolor/22x22/apps', glob.glob('data/icons/hicolor/22x22/apps/*png')),
    ('share/icons/hicolor/24x24/apps', glob.glob('data/icons/hicolor/24x24/apps/*png')),
    ('share/icons/hicolor/32x32/apps', glob.glob('data/icons/hicolor/32x32/apps/*png')),
    ('share/icons/hicolor/48x48/apps', glob.glob('data/icons/hicolor/48x48/apps/*png')),
    ('share/icons/hicolor/scalable/apps', glob.glob('data/icons/hicolor/scalable/apps/*.svg')),
    ('share/pixmaps', glob.glob('data/icons/cconverter.png')),
    ('share/cconverter', glob.glob('data/icons/cconverter.png')),
    ('share/cconverter', glob.glob('data/cconverter.glade')),
    ('share/applications', glob.glob('data/cconverter.desktop')),
    ('share/man/man1', glob.glob('docs/man/cconverter.1')),
]
setup(
    name='cconverter',
    version=app_info.version,
    author=app_info.author_name,
    author_email=app_info.author_email,
    url='http://folk.ntnu.no/einaru/linux',
    description=app_info.description,
    license=app_info.license,
    keywords='currency exchange rate',
    scripts=['bin/cconverter'],
    packages=_packages,
    classifiers=_classifiers,
    data_files=_data_files,
)
