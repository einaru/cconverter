README
******

*Currency Converter* is a simple application for converting currencies. It is
written is Python_ and can be run both as a console application and a graphical
application. The main graphical user interface is written in Gtk+ 3 making use
of the new PyGObject_ bindings. Additionally there exists a graphical 
userinterface written in PyQt4 making use of the new PySide_ bindings.

The application has support for using currency exchangerates from `Yahoo!`_ ,
Google_ and the exchangerate-api.com_ webservices.

*Currency Converter* is developed on Linux and is primarily targeting the
GNOME_ desktop environment, but should run equaly well on platforms with the
necessary dependencies available.


.. _Python: http://www.python.org
.. _PyGObject: https://live.gnome.org/PyGObject
.. _PySide: http://www.pyside.org
.. _Yahoo!: http://finance.yahoo.com/
.. _Google: http://finance.google.com/
.. _exchangerate-api.com: http://www.exchangerate-api.com
.. _GNOME: http://www.gnome.org


Installation
============

No installation procedure is available at the moment. A standard autotools
``./configure ; make ; sudo make install`` is planned though. The only way of
running the application at the moment, is to run it from source, either by 
downloading a tarball or cloning the gitrepo::

    git clone https://github.com/ebethron/cconverter


Example usage::

    $ cconverter.py --help
    Usage: cconverter.py [OPTIONS] ORIGINAL TARGET VALUE
    
    Options:
      -h, --help     show this help message and exit
      -v, --verbose  Print more information to console.
      -l, --list     Print a list of supported currecies to console and exit.
      -g, --gtk      Launch the Gtk user interface.
      -q, --qt       Launch the Qt4 user interface.
    
    $ cconverter.py USD NOK 100
    533.82
    $ cconverter.py --gtk
    $ cconverter.py --qt

 
Supported Currencies
====================

.. csv-table:: "Supported Currencies"
   :file: https://github.com/ebethron/cconverter/raw/master/data/currencies.csv
   :header: "Country", "ISO-3166", "Currency", "ISO-4217"


Screenshots
===========

|main| |prefs| |calc| |about|

.. |main| image:: https://github.com/ebethron/cconverter/raw/master/help/C/figures/CConverter-0.4.png
.. |prefs| image:: https://github.com/ebethron/cconverter/raw/master/help/C/figures/CConverter-0.4_preferences.png
.. |calc| image:: https://github.com/ebethron/cconverter/raw/master/help/C/figures/CConverter-0.4_calc.png
.. |about| image:: https://github.com/ebethron/cconverter/raw/master/help/C/figures/CConverter-0.4_about.png


License
=======
*Currency Converter* is licensed under the terms of the GNU General Public 
License (GPL) version 3 or later.
