# -*- coding: utf-8 -*-
"""
:Date: Wed Jul 27 02:21:55 CEST 2011
:Authors: Einar Uvsløkk <einar.uvslokk@linux.com>
:Copyright: (c) 2011 Einar Uvsløkk
:License: GNU General Public License (GPL) version 3 or later

vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
import logging
import operator
import urllib
import sys
from gettext import gettext as _

__all__ = ['CurrencyConverter', 'pprint_currencies', 'Currencies']

Currencies = {
    'ARS': ['Argentine Peso',                'Argentina',            'ar'],
    'AUD': ['Australian Dollar',             'Australia',            'au'],
    'BSD': ['Bahamian Dollar',               'Bahamas',              'bs'],
    'BHD': ['Bahraini Dinar',                'Bahrain',              'bh'],
    'BBD': ['Barbados Dollar',               'Barbados',             'bb'],
    'XOF': ['Cfa Franc Bceao',               'Benin',                'bj'],
    'BRL': ['Brazilian Real',                'Brazil',               'br'],
    'XAF': ['Cfa Franc Beac',                'Cameroon',             'cm'],
    'CAD': ['Canadian Dollar',               'Canada',               'ca'],
    'CLP': ['Chilean Peso',                  'Chile',                'cl'],
    'CNY': ['Chinese Yuan',                  'China',                'cn'],
    'HRK': ['Croatia Kuna',                  'Croatian',             'hr'],
    'CZK': ['Czech Koruna',                  'Czech Republic',       'cz'],
    'DKK': ['Danish Krone',                  'Denmark',              'dk'],
    'XCD': ['East Caribbean Dollar',         'East Caribbean',       'dm'],
    'EGP': ['Egyptian Pound',                'Egypt',                'eg'],
    'EEK': ['Estonian Kroon',                'Estonia',              'ee'],
    'EUR': ['Euro',                          'Eurozone',             'eu'],
    'FJD': ['Fiji Dollar',                   'Fiji',                 'fj'],
    'HKD': ['Hong Kong Dollar',              'Hong Kong',            'hk'],
    'HUF': ['Hungarian Forint',              'Hungary',              'hu'],
    'ISK': ['Icelandic Krona',               'Iceland',              'is'],
    'INR': ['Indian Rupee',                  'India',                'in'],
    'IDR': ['Indonesian rupiah',             'Indonesia',            'id'],
    'ILS': ['Israeli New Shekel',            'Israel',               'il'],
    'JMD': ['Jamaican Dollar',               'Jamaica',              'jm'],
    'JPY': ['Japanese Yen',                  'Japan',                'jp'],
    'KES': ['Kenyan Shilling',               'Kenya',                'ke'],
    'KRW': ['Korean Won',                    'Korea',                'kp'],
    'LVL': ['Latvian Lats',                  'Latvia',               'lv'],
    'LTL': ['Lithuanian Litas',              'Lithuania',            'lt'],
    'MYR': ['Malaysian Ringgit',             'Malaysia',             'my'],
    'MXN': ['Mexican Pesos',                 'Mexico',               'mx'],
    'MAD': ['Moroccan Dirham',               'Morocco',              'ma'],
    'ANG': ['Netherlands Antillian Guilder', 'Netherlands Antilles', 'an'],
    'NZD': ['New Zealand Dollar',            'New Zealand',          'nz'],
    'NOK': ['Norwegian Krone',               'Norway',               'no'],
    'OMR': ['Omani Rial',                    'Oman',                 'om'],
    'PKR': ['Pakistani Rupee',               'Pakistan',             'pk'],
    'PAB': ['Panamanian Balboa',             'Panama',               'pa'],
    'PEN': ['Peruvian Nuevo Sol',            'Peru',                 'pe'],
    'PHP': ['Philippine Peso',               'Philippines',          'ph'],
    'PLN': ['Polish Zloty',                  'Poland',               'pl'],
    'QAR': ['Qatari Rial',                   'Qatar',                'qa'],
    'RON': ['New Romanian Leu',              'Romania',              'ro'],
    'RUB': ['Russian Rouble',                'Russia',               'ru'],
    'SAR': ['Saudi Riyal',                   'Saudi Arabia',         'sa'],
    'RSD': ['Serbian Dinar',                 'Serbia',               'rs'],
    'SGD': ['Singapore Dollar',              'Singapore',            'sg'],
    'ZAR': ['South African Rand',            'South Africa',         'za'],
    'LKR': ['Sri Lanka Rupee',               'Sri Lanka',            'lk'],
    'SEK': ['Swedish Krona',                 'Sweden',               'se'],
    'CHF': ['Swiss Franc',                   'Switzerland',          'ch'],
    'TWD': ['Taiwan New Dollar',             'Taiwan',               'tw'],
    'THB': ['Thai Baht',                     'Thailand',             'th'],
    'TTD': ['Trinidad And Tobago Dollar',    'Trinidad and Tobago',  'tt'],
    'TRY': ['New Turkish Lira',              'Turkey',               'tr'],
    'AED': ['Uae Dirham',                    'United Arab Emirates', 'ae'],
    'GBP': ['Pound Sterling',                'United Kingdom',       'uk'],
    'USD': ['US Dollar',                     'United States',        'us'],
    'VEF': ['Venezuelan Bolivar Fuerte',     'Venezuela',            've'],
    'VND': ['Vietnamese Dong',               'Viet Nam',             'vn']}
"""The following currency codes are supported by this API:

http://exchangerate-api.com/supported-currencies
"""

_log = logging.getLogger(__name__)


def pprint_currencies(out=sys.stdout):
    """Pretty print all supported currencies."""
    strf = '{:<30} {:<30} {}'
    for k, v in sorted(Currencies.items(), key=operator.itemgetter(1)):
        print >> out, strf.format(v[1], v[1], k)


class CurrencyPair:
    def __init__(self, source, target, exrate):
        self.source = source
        self.target = target
        self.exrate = exrate


class CurrencyConverter(object):
    def __init__(self, api='yahoo'):
        self._api = api

    def get_conversion_matrix(self, currencies=[]):
        size = len(currencies)
        pairs = []
        for i in xrange(size):
            for j in xrange(size):
                pairs.append(CurrencyPair(currencies[i], currencies[j]))

        self.convert(pairs)
        matrix = [[None] * size for i in xrange(size)]

        index = 0
        for i in xrange(size):
            for j in xrange(size):
                matrix[i][j] = pairs[index] if i != j else None
                index += 1

        return matrix

    def convert(self, source, target, value):
        rate = self.exchangerate(source, target)
        return (rate * float(value), rate)

    def exchangerate(self, source, target):
        if 'yahoo' == self._api:
            return YahooAPI.exchangerate(source, target)
        elif 'google' == self._api:
            return GoogleAPI.exchangerate(source, target)
        elif 'exchangerate-api' == self._api:
            return ExchangerateAPI.exchangerate(source, target)

    def get_api(self):
        return self._api

    def set_api(self, api):
        if api != self._api:
            _log.info('API changed from {} to {}'.format(self._api, api))
            self._api = api

    api = property(get_api, set_api)


class YahooAPI:
    @staticmethod
    def exchangerate(source, target):
        url = 'http://download.finance.yahoo.com/d/quotes.csv?{}f=l1&e=.cs'
        var = 's={source}{target}=X&'.format(source=source, target=target)
        rate = urllib.urlopen(url.format(var)).read()
        try:
            rate = float(rate)
        except ValueError as e:
            _log.error(format(e))
            raise ApiError(1, _('Unknown Yahoo! API error occured'))

        msg = 'Yahoo! API response: {} -> {} = {}'
        _log.info(msg.format(source, target, rate))
        return rate


class GoogleAPI:
    @staticmethod
    def exchangerate(source, target):
        url = 'http://www.google.com/ig/calculator?hl=en&q=1{source}=?{target}'
        url = url.format(source=source, target=target)
        response = urllib.urlopen(url).read()
        # Hacky Hack Hackerson
        data = response.split('"')
        rate = data[3].split(' ')[0]
        error = data[5]
        if error != '':
            try:
                error = int(error)
            except ValueError as e:
                _log.error(format(e))
                raise ApiError(1, format(error))

            if error == 1:
                _log.debug('Document Google Api Error code 1')
            if error == 2:
                _log.debug('Document Google Api Error code 2')
            if error == 2:
                _log.debug('Document Google Api Error code 3')
            if error == 3:
                _log.debug('Document Google Api Error code 4')
            if error == 4:
                raise GoogleApiError(error, _('Invalid currency code used'))

        try:
            rate = float(rate)
        except ValueError as e:
            _log.error(format(e))
            raise ApiError(1, _('Unknown Google API error occured'))

        msg = 'Google API response: {} -> {} = {}'
        _log.info(msg.format(source, target, rate))
        print type(rate)
        return rate


class ExchangerateAPI:
    @staticmethod
    def exchangerate(source, target):
        url = 'http://www.exchangerate-api.com/{source}/{target}?k={key}'
        url = url.format(source=source, target=target, key='bfzYQ-YE2vb-dckeY')
        rate = urllib.urlopen(url).read()
        try:
            rate = float(rate)
        except ValueError as e:
            _log.error(format(e))
            raise ExchangerateApiError(6, _('Unkown error occured'))

        if rate == '-1':
            raise ExchangerateApiError(rate, _('Invalid amount used.'))
        if rate == '-2':
            raise ExchangerateApiError(rate, _('Invalid currency code used.'))
        if rate == '-3':
            raise ExchangerateApiError(rate, _('Invalid API key is used.'))
        if rate == '-4':
            raise ExchangerateApiError(rate, _('API query limit reached.'))
        if rate == '-5':
            raise ExchangerateApiError(rate, _('Unresolved IP address used.'))

        msg = 'Exchangerate API response: {} -> {} = {}'
        _log.info(msg.format(source, target, rate))
        return rate


class ApiError(Exception):
    def __init__(self, value, msg):
        self.value = abs(value)
        self.msg = msg

    def __repr__(self):
        reprf = '<ApiError value="{}" message="{}">'
        return reprf.format(self.value, self.msg)

    def __str__(self):
        return '[Api Error] {}'.format(self.msg)


class YahooApiError(ApiError):
    def __str__(self):
        return '[Yahoo! Api Error] {}'.format(self.msg)


class GoogleApiError(ApiError):
    def __str__(self):
        return '[Google Api Error] {}'.format(self.msg)


class ExchangerateApiError(ApiError):
    def __str__(self):
        return '[Exchangerate Api Error] {}'.format(self.msg)
