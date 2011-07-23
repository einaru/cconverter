# -*- coding: utf-8 -*-
"""
:Date: Fri Jul 22 17:20:01 CEST 2011
:Authors: Einar Uvsløkk <einar.uvslokk@linux.com>
:Copyright: (c) 2011 Einar Uvsløkk
:License: GNU General Public License (GPL) version 3 or later

vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""


def run(config, ui):
    if ui == 'gtk':
        from .gui.window import main
        main(config)
