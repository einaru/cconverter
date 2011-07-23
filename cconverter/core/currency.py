# -*- coding: utf-8 -*-
"""
:Date: Fri Jul 22 15:40:30 CEST 2011
:Authors: Einar Uvsløkk <einar.uvslokk@linux.com>
:Copyright: (c) 2011 Einar Uvsløkk
:License: GNU General Public License (GPL) version 3 or later

vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
import urllib


API_KEY = 'bfzYQ-YE2vb-dckeY'
API_URL = 'http://www.exchangerate-api.com'

currencies = {
    'Australian Dollar': 'AUD',
    'Brazilian Real': 'BRL',
    'British Pound Sterling': 'GBP',
    'Bulgarian Lev': 'BGN',
    'Canadian Dollar': 'CAD',
    'Chinese Yuan': 'CNY',
    'Croatia Kuna': 'HRK',
    'Czech Koruna': 'CZK',
    'Danish Krone': 'DKK',
    'Estonian Kroon': 'EEK',
    'Euro': 'EUR',
    'Hong Kong Dollar': 'HKD',
    'Hungarian Forint': 'HUF',
    'Indonesian rupiah': 'IDR',
    'Japanese Yen': 'JPY',
    'Korean Won': 'KRW',
    'Latvian Lats': 'LVL',
    'Lithuanian Litas': 'LTL',
    'Malasian Ringgit': 'MYR',
    'Mexican Pesos': 'MXN',
    'New Romanian Leu': 'RON',
    'New Turkish Lira': 'TRY',
    'New Zealand Dollar': 'NZD',
    'Norwegian Krone': 'NOK',
    'Philippine Peso': 'PHP',
    'Polish Zloty': 'PLN',
    'Russian Rouble': 'RUB',
    'Singapore Dollar': 'SGD',
    'South African Rand': 'ZAR',
    'Swedish Krona': 'SEK',
    'Swiss Franc': 'CHF',
    'Thai Baht': 'THB',
    'US Dollar': 'USD'}
"""The following currency codes are supported by this API:

http://exchangerate-api.com/supported-currencies
"""


def print_currencies():
    """Print all supported currencies with currency identificators."""
    for k, v, in sorted(currencies.items()):
        print v, k


def convert(amount, from_c, to_c):
    """Convert an amount from `from_c` to `to_c`.

    Returns the exchangerate or an error message if `amount` is
    non-numeric.

    :param amount: The amount to convert
    :type amount: float
    :param from_c: The currency identificator to convert from
    :type from_c: string
    :param to_c: The currency identificator to covnert to
    :type to_c: string
    :rtype: string
    """
    try:
        amount = float(amount)
    except ValueError:
        return 'Invalid input: Must be numeric!'

    url = '{}/{}/{}/{}?k={}'.format(API_URL, from_c, to_c, amount, API_KEY)
    response = urllib.urlopen(url)
    return response.read()


def exchangerate(from_c, to_c):
    """Get the rate between to currencies

    :param from_c: The currency to check
    :type from_c: string
    :param to_c: The currency to check against
    :type to_c: string
    :rtype: string
    """
    url = '{}/{}/{}/?k={}'.format(API_URL, from_c, to_c, API_KEY)
    response = urllib.urlopen(url)
    return response.read()
