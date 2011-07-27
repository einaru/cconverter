# -*- coding: utf-8 -*-
"""
:Date: Sun Jul 24 20:04:16 CEST 2011
:Authors: Einar Uvsløkk <einar.uvslokk@linux.com>
:Copyright: (c) 2011 Einar Uvsløkk
:License: GNU General Public License (GPL) version 3 or later

vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
from PySide.QtCore import QSize
from PySide.QtGui import QIcon


def iconFromTheme(icon, fallback):
    """ Utility method for getting icons from default X11 icon theme.

    Returns a ``QIcon`` from the X11 system-icon theme if a match is
    found, else the `fallback` is used.

    :param icon: the name of the icon in the X11 icon-theme.
    :type icon: string
    :param fallback: the name of the fallback icon.
    :type icon: string
    """
    return QIcon.fromTheme(icon, QIcon(fallback))


def pixmapFromTheme(icon, fallback, width=48, height=48, mode=QIcon.Normal,
                    state=QIcon.Off):
    """Utility method for converting a ``QIcon`` to a ``QPixmap``.
    Useful when trying to use icons from a X11 iconTheme but need a
    pixmap.

    Returns a ``QPixmap`` from the X11 system icon-theme if a match is
    found, else the `fallback` is used.

    :param icon: the name of the icon in the icon theme.
    :type icon: string
    :param fallback: the name of the fallback icon.
    :type fallback: string
    :param widht: the width of the icon, default is 48.
    :type width: int
    :param height: the height of the icon, default is 48.
    :type height: int
    :param mode: the icon mode, default is ``QIcon.Normal``,
    :type mode: see http://doc.trolltech.com/4.7/qicon.html#Mode-enum
    :param state: the icon state, default is ``QIcon.Off``,
    :type state: see http://doc.trolltech.com/4.7/qicon.html#State-enum
    """
    ret = iconFromTheme(icon, fallback)
    return ret.pixmap(QSize(width, height), QIcon.Normal, QIcon.Off)
