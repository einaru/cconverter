# -*- coding: utf-8 -*-
"""
:Date: Fri Jul 22 17:20:01 CEST 2011
:Authors: Einar Uvsløkk <einar.uvslokk@linux.com>
:Copyright: (c) 2011 Einar Uvsløkk
:License: GNU General Public License (GPL) version 3 or later

vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
import logging
import sys
from optparse import OptionParser

from core import currency


def cconverter(args):
    converter = currency.CurrencyConverter()
    if len(args) == 2:
        try:
            print >> sys.stdout, converter.exchangerate(*args)
        except currency.Error as e:
            print >> sys.stderr, str(e)
            return e.value

    elif len(args) == 3:
        try:
            print >> sys.stdout, converter.convert(*args)[0]
        except currency.Error as e:
            print >> sys.stderr, str(e)
            return e.value

    elif len(args) < 2:
        print >> sys.stderr, 'Invalid number of arguments'
        return 1

    return 0


def run(data):
    usage = 'Usage: %prog [OPTIONS] ORIGINAL TARGET VALUE'
    parser = OptionParser(usage=usage)
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      help='Print more information to console.')
    parser.add_option('-l', '--list', dest='list', action='store_true',
                      help='Print a list of supported currecies to console '
                           'and exit.')
    parser.add_option('-g', '--gtk', dest='gtk', action='store_true',
                      help='Launch the Gtk user interface.')
    parser.add_option('-q', '--qt', dest='qt', action='store_true',
                      help='Launch the Qt4 user interface.')

    (opt, args) = parser.parse_args()

    #logger = logging.getLogger()
    #logger.setLevel(logging.INFO)
    #formatter = logging.Formatter('%(levelname)-8s: %(message)s')

    if opt.verbose:
        logging.basicConfig(
            level=logging.INFO,
            format='%(levelname)-8s: %(name)s: %(message)s'
        )

    if opt.list:
        print >> sys.stdout, 'List of supported currencies'
        print >> sys.stdout, '----------------------------'
        currency.pprint_currencies()
        sys.exit(0)

    if opt.gtk:
        from .gui.window import main
    elif opt.qt:
        from .qt.window import main
    else:
        sys.exit(cconverter(args))

    main(data)
    sys.exit(0)
