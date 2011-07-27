# -*- coding: utf-8 -*-
"""
:Date: Sun Jul 24 18:11:38 CEST 2011
:Authors: Einar Uvsløkk <einar.uvslokk@linux.com>
:Copyright: (c) 2011 Einar Uvsløkk
:License: GNU General Public License (GPL) version 3 or later

vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
import ConfigParser
import logging
import os
from xdg import BaseDirectory


class Config(object):
    """A simple Config object."""
    _log = logging.getLogger(__name__)

    def __init__(self):
        self._source_currency = 'AUD'
        self._target_currency = 'AUD'
        self._resource_api = ''
        self._check_location()

    def _check_location(self):
        """Basic check to ensure we have a valid fileobject to work with
        for the `ConfigParser` object.
        """
        try:
            prefix = os.path.join(BaseDirectory.xdg_config_home, 'cconverter')
        except ImportError:
            prefix = os.path.join(os.environ['HOME'], '.config', 'cconverter')

        if not os.path.exists(prefix):
            try:
                os.mkdir(prefix)
            except (IOError, OSError):
                import tempfile
                old = prefix
                prefix = tempfile.gettempdir()
                msg = 'Could not create config directory: {old}. ' \
                      'Using unpersistent config location: {tmp}'
                self._log.warning(msg.format(old=old, tmp=prefix))

        self.filename = os.path.join(prefix, 'config.ini')
        self._log.debug('Configuration location: {}'.format(self.filename))

    def write(self):
        config = ConfigParser.ConfigParser()
        config.add_section('currency')
        config.set('currency', 'api', self._resource_api)
        config.set('currency', 'source', self._source_currency)
        config.set('currency', 'target', self._target_currency)
        config.write(open(self.filename, 'w'))

    def read(self):
        config = ConfigParser.ConfigParser()
        config.read(self.filename)
        if config.has_section('currency'):
            self._resource_api = config.get('currency', 'api')
            self._source_currency = config.get('currency', 'source')
            self._target_currency = config.get('currency', 'target')

    def get_source_currency(self):
        return self._source_currency

    def set_source_currency(self, value):
        self._source_currency = value

    source = property(get_source_currency, set_source_currency)

    def get_target_currency(self):
        return self._target_currency

    def set_target_currency(self, value):
        self._target_currency = value

    target = property(get_target_currency, set_target_currency)

    def get_api(self):
        return self._resource_api

    def set_api(self, value):
        self._resource_api = value

    api = property(get_api, set_api)
