#!/usr/bin/env python
"""
Parsing functionality for schema matching.
Includes generic methods to extract common field types, e.g date/time, price listings, 
addresses etc.
"""

import re
import sys
import logging
from time import time
from datetime import datetime

import pytz
import dateutil.parser
from pyparsing import alphas, nums
from pyparsing import (Word, Suppress, Group, 
                       Optional, OneOrMore, oneOf, Literal,
                       CaselessLiteral, stringEnd, ParseException)

from wind.parsing.errors import ParsingFailed

def datetime_grammar():
    """Define grammar for parsing datetime
    strings mixed with arbitrary date"""
    CL = CaselessLiteral

    COLON = Suppress(':')
    SLASH = Suppress('/')
    DOT   = Suppress('.')
    COMMA = Suppress(',')

    am = CL("am")
    pm = CL("pm")    

    ignoreWord = Suppress(Word(alphas+nums+":;,()"))

    integer = Word(nums).setParseAction(lambda t: int(t[0])) 
    int2 = Word(nums,exact=2).setParseAction(
        lambda t: int(t[0]) )
    int4 = Word(nums,exact=4).setParseAction(
        lambda t: int(t[0]) )
    split_int4 = Group(Word(nums,exact=4).setParseAction(
        lambda t: [int(t[0][:2]),int(t[0][2:])] ))

    tz = oneOf(['PDT', 'PST', 'EDT', 'CDT'])

    timespec = Group(split_int4("miltime") |
                     integer("hour") + 
                     Optional(COLON + integer("minutes")) + 
                     Optional(COLON + integer("seconds")) + 
                     Optional((am | pm)("ampm"))
                     )
    datespec = Group(integer("month") + (SLASH | DOT) + integer("day") +
                     Optional((SLASH | DOT) + integer("year")))

    tzspec = Group(tz)

    parser = OneOrMore(timespec("timespec") ^
                       datespec("datespec") ^
                       tzspec("tzspec") ^
                       ignoreWord) + stringEnd

    return parser

def notempty(s):    
    if not s:
        raise ValueError("Value was empty in nonempty() schema rule")
    return s

def notequal(s, v):
    """Raises exception for attribute
    if its value equals given one in v"""
    if s == v:
        raise ValueError("notequal() - Value was prohibited: %s" % v)
    return s

def const(s):
    """Return literal value"""
    return s

def lower(s):
    """Lower case string"""
    return s.lower()

def upper(s):
    """Upper case string"""
    return s.upper()

def parse_time(s, fmt=None, t_re=None, **kwargs):
    """Parse a time segment (e.g '8:30am', '21:30') out of string"""

def parse_date(s, fmt=None, d_re=None, **kwargs):
    """Parse a date segment (e.g '21.10', '03/15/1985') from string"""

def parse_datetime(s, fmt=None, dt_re=None, string=True, **kwargs):
    """Try to parse a datetime from given string.
    no timezone information is applied by default
    is not provider.

    Args:
      s - String containing datetime info to extract
      fmt - datetime format string. If given, will be used
        to parse the string.
      dt_re - RegExp with named clauses to parse string.
        If given, will be used to parse the string
      string - Return result as string (isoformat()) or as 
        datetime object

      kwargs - Can given date completion information, e.g
        values to interpolate for 'year', 'month', 'hour' etc.
    """

    if fmt is not None:
        return datetime.strptime(s, fmt)
    elif dt_re is not None:
        matches = re.search(dt_re, s)
        if not matches:
            return None

    # Try to automatically extract
    dt=None
    try:
        dt = dateutil.parser.parse(s)
    except ValueError, exc:
        # Could not parse with dateutil,
        # try our recursive decent parser and heuristics
        parser = datetime_grammar()
        try:
            tokens = parser.parseString(s)
        except ParseException:
            logging.exception("ParseException while tring to parse datetime string: %s", s)
        else:
            # Parse into datetime object
            now = datetime.now()
            _dt_attrs = {}
            if tokens.datespec:
                if 'year' in tokens.datespec:
                    if tokens.datespec['year'] < 1000:
                        # Two-digit year format, correct.
                        # NOTE: This correction will only be valid
                        # for the next thousand years :)
                        tokens.datespec['year'] += 2000
                for k in ('year', 'month', 'day'):
                    if getattr(tokens.datespec, k):
                        _dt_attrs[k] = tokens.datespec[k]
                    elif k in kwargs:
                        # User supplied 
                        _dt_attrs[k] = kwargs[k]
                    else:
                        # Default to now
                        _dt_attrs[k] = getattr(now, k)

            if tokens.timespec:
                _hour = tokens.timespec.hour
                if tokens.timespec.ampm:
                    if tokens.timespec.ampm == 'pm' \
                       and _hour < 13:
                        # Adjust hour format
                        _hour = (_hour+12) % 24
                _dt_attrs['hour'] = _hour

                if tokens.timespec.minutes:
                    _dt_attrs['min'] = tokens.timespec.minutes
                else:
                    _dt_attrs['min'] = 0

                if tokens.timespec.seconds:
                    _dt_attrs['sec'] = tokens.timespec.seconds
                else:
                    _dt_attrs['sec'] = 0


            dt = datetime(_dt_attrs['year'], 
                          _dt_attrs['month'], 
                          _dt_attrs['day'], 
                          _dt_attrs['hour'], 
                          _dt_attrs['min'], 
                          _dt_attrs['sec'])

    if not dt:
        # Could not parse
        raise ParsingFailed("Could not extract datetime from attribute: '%s'" \
                            % s)

    if string is True:
        return dt.isoformat()
    return dt

def parse_address(s, address_re=None, **kwargs):
    """Try to parse an address field,
    mapping it to common fields like street address, 
    city, state, country, zipcode etc."""
    pass

def parse_price(s, price_re=None, **kwargs):
    """Try to parse a price field,
    extracting value as well as currency if available"""
    pass
