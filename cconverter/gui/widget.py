# -*- coding: utf-8 -*-
"""
:Date: Fri Jul 22 16:19:36 CEST 2011
:Authors: Einar Uvsløkk <einar.uvslokk@linux.com>
:Copyright: (c) 2011 Einar Uvsløkk
:License: GNU General Public License (GPL) version 3 or later

vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
from gettext import gettext as _
from gi.repository import Gtk


class Calculator(Gtk.Table):

    def __init__(self, view, *args, **kwargs):
        super(Calculator, self).__init__(*args, **kwargs)
