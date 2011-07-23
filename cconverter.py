#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Date: Thu Jun 30 17:17:35 CEST 2011
:Version: 1
:Authors: Einar Uvsløkk <einar.uvslokk@linux.com>
:Copyright: (c) 2011 Einar Uvsløkk 
:License: GNU General Public License (GPL) version 3 or later

vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
import gettext
import locale
import logging
import os

import cconverter
from cconverter import app

try:
    from etrainer.defs import (DATA_DIR, PKG_DATA_DIR, LOCALE_DIR)
    DEFS_PRESENT = True
except ImportError:
    DATA_DIR = PKG_DATA_DIR = LOCALE_DIR = ''
    DEFS_PRESENT = False

if not DEFS_PRESENT:
    _prefix = '/usr'
    DATA_DIR = os.path.join(_prefix, 'share')
    LOCALE_DIR = os.path.join(_prefix, 'share', 'locale')
    _me = os.path.abspath(os.path.dirname(__file__))
    PKG_DATA_DIR = os.path.join(_me, 'data')

cconverter.DATA_DIR = DATA_DIR
cconverter.PKG_DATA_DIR = PKG_DATA_DIR
cconverter.LOCALE_DIR = LOCALE_DIR
cconverter.APP_NAME = 'cconverter'

logging.basicConfig(format='%(levelname)-8s: %(message)s', level=logging.INFO)

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain(cconverter.APP_NAME, LOCALE_DIR)
gettext.textdomain(cconverter.APP_NAME)
gettext.install(cconverter.APP_NAME)

dirs = {'DATA_DIR': DATA_DIR,
        'PKG_DATA_DIR': PKG_DATA_DIR,
        'LOCALE_DIR': LOCALE_DIR,}
kwargs = {'ui': 'gtk', 'config': dirs,}
app.run(**kwargs)
