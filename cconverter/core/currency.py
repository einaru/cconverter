#!/bin/env python
#-*- coding: utf-8 -*-
# 
# currency
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
import urllib

"""
API location: http://exchangerate-api.com/supported-currencies

The required Api Key:
"""
API_KEY="bfzYQ-YE2vb-dckeY"

"""
The following currency codes are supported by this API:
"""
currencies = {
    "Australian Dollar" : "AUD",    #  0
    "Brazilian Real" : "BRL",       #  1
    "Bulgarian Lev" : "BGN",        #  2
    "Canadian Dollar" : "CAD",      #  3
    "Chinese Yuan" : "CNY",         #  4
    "Croatia Kuna" : "HRK",         #  5
    "Czech Koruna" : "CZK",         #  6
    "Danish Krone" : "DKK",         #  7
    "Estonian Kroon" : "EEK",       #  8
    "Euro" : "EUR",                 #  9
    "Hong Kong Dollar" : "HKD",     # 10
    "Hungarian Forint" : "HUF",     # 11
    "Indonesian rupiah" : "IDR",    # 12
    "Japanese Yen" : "JPY",         # 13
    "Korean Won" : "KRW",           # 14
    "Latvian Lats" : "LVL",         # 15
    "Lithuanian Litas" : "LTL",     # 16
    "Malasian Ringgit" : "MYR",     # 17
    "Mexican Pesos" : "MXN",        # 18
    "New Romanian Leu" : "RON",     # 19
    "New Turkish Lira" : "TRY",     # 20
    "New Zealand Dollar" : "NZD",   # 21
    "Norwegian Krone" : "NOK",      # 22
    "Philippine Peso" : "PHP",      # 23
    "Polish Zloty" : "PLN",         # 24
    "Pound Sterling" : "GBP",       # 25
    "Russian Rouble" : "RUB",       # 26
    "Singapore Dollar" : "SGD",     # 27
    "South African Rand" : "ZAR",   # 28
    "Swedish Krona" : "SEK",        # 29
    "Swiss Franc" : "CHF",          # 30
    "Thai Baht" : "THB",            # 31
    "US Dollar" : "USD",            # 32
}

def print_currencies():
    """
    Print all supported currencies with currency identificators
    """
    for k, v, in sorted(currencies.items()):
        print v, k


def convert(from_c, to_c, amount):
    """
    Convert an amount from currency to currency
    
    @param from_c: The currency to convert from
    @param to_c: The currency to covnert to
    @param amount: The amount to convert
    @return: The exchangerate
    """
    try:
        amount = float(amount)
    except ValueError:
        return "Invalid input: Must numeric!"
    url = urllib.urlopen("http://www.exchangerate-api.com/%s/%s/%f?k=%s" % \
                         (from_c, to_c, amount, API_KEY))
    return url.read()

def get_exchangerate(from_c, to_c):
    """
    Get the rate between to currencies
    
    @param from_c: The currency to check
    @param to_c: The currency to check against
    @return: The exchangerate
    """
    url = urllib.urlopen("http://www.exchangerate-api.com/%s/%s/?k=%s" % \
                         (from_c, to_c, API_KEY))
    return url.read()
