==========
cconverter
==========

-------------------------------------
Simple currency converter application
-------------------------------------

:Date:           Sun Jul 24 14:12:58 CEST 2011
:Copyright:      GNU General Public License version 3 or later
:Manual section: 1
:Manual group:   Finance

SYNOPSIS
========
cconverter [OPTIONS] ORIGINAL TARGET VALUE


DESCRIPTION
===========
*cconverter* is a simple application for converting currecies. It can be run
from the console or as a Gtk application. It uses the *exchangerate-api.com* 
webservice to convert the various currencies. A list of supported currecies
can be seen by running the application with the `--list` flag.


OPTIONS
=======
A summary of the options supported by *cconverter* is included below:

-h, --help
    Display a help message and exit.

-v, --verbose
    Print more information to console.

-l, --list
    Print a list of supported currencies to console and exit.

-g, --gtk
    Launch the Gtk user interface.

-q, --qt
    Launch the Qt4 user interface.


FILES
=====
``~/.config/cconverter/``
    Default directory for configuration data.

``~/.config/cconverter/config.ini``
    Main configuration file.


BUGS
====
Bug tracker: https://github.com/ebethron/cconverter/issues

RESOURCES
=========
Website: https://github.com/ebethron/cconverter
Yahoo! finance: http://finance.yahoo.com
Google finance: http://finance.google.com
Exchangerates: http://www.exchangerate-api.com/


AUTHORS
=======
Einar Uvsløkk <einar.uvslokk@linux.com>
