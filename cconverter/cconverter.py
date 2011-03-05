#!/bin/env python
#-*- coding: utf-8 -*-
#
# cconverter
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
import sys
import optparse

from core.currency import convert, get_exchangerate, print_currencies
from core.app_info import description, logo, name, version
from gui import cconverter_gtk

def main():
    p = optparse.OptionParser(
                description=description,
			    version="%s %s" % (name, version),
			    usage="Usage: %prog [options] FROM TO AMOUNT")
    p.add_option("--gtk",
                action="store_true",
                dest="gtk",
                help="Run the gtk gui")
    p.add_option("-r", "--rate",
			    action="store_true",
			    dest="rate",
			    help="apply this to omitt the amount. Returns the current exhange-rate")
    p.add_option("-c", "--currencies",
                action="store_true",
                help="Display the list of supported currencies")

    (options, args) = p.parse_args()

    if options.gtk:
        cconverter_gtk.main()
        sys.exit(1)
    if options.currencies:
        print_currencies()
        sys.exit(1)

    if len(args) < 2:
        print logo
        p.print_help()
        sys.exit(1)

    # TODO add a -v option to be verbose
    if options.rate:
        print get_exchangerate(args[0], args[1])
    else:
        if len(args) > 2:
            print convert(args[0], args[1], args[2])

if __name__ == "__main__":
    main()
