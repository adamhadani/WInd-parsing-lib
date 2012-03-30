#!/usr/bin/env python
"""Test parsers functionality"""
import logging
import unittest
from time import time
from datetime import datetime

from pytz import timezone

from wind.parsing import *

logging.basicConfig(level=logging.DEBUG)

#class GrammarTestCase(unittest.TestCase):
#    """Test Grammar / parsing functionality"""
#    
#    def testGrammar(self):
#        mapper = SchemaMapper()
#        _mapping = {'datetime': 'time + date', 'title': 'title'}
#        _mapped = mapper.map_item({'title': 'Moo', 'time': '8:00 PM Doors', 
##                          'date': '21.11'}, _mapping)
#        self.assertEquals(len(_mapped), len(_mapping), \
#                          "Output length did not match mapping")
        
        
class ParsingTestCase(unittest.TestCase):
    """Test Schem Matching module"""
        
    def testDateTimeGrammar(self):
        parser = datetime_grammar()
        test_set = [
            ('10.21 Show 11:00 PM', None),
            ('8pm', None),
            ('10/24/2010 21:30', None),
            ('Doors Open 09:30, Show Starts 11pm', None),
            ('Thu, 12/02/10 8:00', datetime(2010, 12, 02, 8, 00)),
            ('Thu, 12/02/10 8:00 PM', datetime(2010, 12, 02, 20, 00)),
            ('Thu, 12/02/10 8:00 PM PST', datetime(2010, 12, 02, 20, 00)),
            ('Thu, 12/02/10 8:00 PM PST (7:00 PM DOORS)', datetime(2010, 12, 02, 20, 00))
            ]
        for s, dt_obj in test_set:
            try:
                tokens = parser.parseString(s)
            except ParseException:
                logging.exception("Parsing failed for string: %s", s)
                raise
            self.assertNotEqual(None, tokens, "Could not parse string: %s" \
                                % s)

        
    def testParseDateTime(self):
        dtnow = datetime.now()
        year = dtnow.year
        test_set = [
            ('Oct 29, 2010, 9:00 PM', datetime(2010, 10, 29, 21, 00)),
            ('10.21 Show 11:00 PM', datetime(year, 10, 21, 23, 00)),
            ('8pm', dtnow.replace(hour=20, minute=0, second=0, microsecond=0)),
            ('05/24/2010 21:30', datetime(2010, 5, 24, 21, 30)),
            ('10.30 Doors Open 09:30, Show Starts 11pm', datetime(year, 10, 30, 23, 00)),
            ('10.29.2010 Show 9:00 pm', datetime(2010, 10, 29, 21, 00)),
            ('2010-10-20T19:00-08:00', datetime(2010,10,20,19)),
            ('Nov 20, 2010, 7:30 PM', datetime(2010, 11, 20, 19, 30)),
            ('Show 9:00 pm 1.8', datetime(year, 1, 8, 21)),
            ('Thu, 12/02/10 8:00 PM', datetime(2010, 12, 02, 20, 00)),
            ('Thu, 12/02/10 8:00 PM PST', datetime(2010, 12, 02, 20, 00)),
            ('Thu, 12/02/10 8:00 PM PST (7:00 PM DOORS)', datetime(2010, 12, 02, 20, 00))
            #('2010-11-06T22:00-08:00 (10pm-2am)', datetime(2010, 11, 06, 22)),
            #('2010-11-06 (Sun Nov 6 (9:00pm - 2:00am))', datetime(2010, 11, 06, 21)),
            #('2010-11-06 (9pm till 2am)', datetime(2010, 11, 06, 21))
            
            ]
        
        for s, dt_obj in test_set:
            _dt_obj = parse_datetime(s, string=False)
            self.assertEqual(_dt_obj.replace(tzinfo=None), dt_obj, "Parsed date Got %s, Expected %s for string: '%s'" \
                             % (_dt_obj, dt_obj, s))
            
    def testParseDateTimeMemory(self):
        dtnow = datetime.now()
        test_set = [
            ('10.21 Show 11:00 PM', datetime(2010, 10, 21, 23, 00)),
            ('10.25 Show 11:00 PM', datetime(2010, 10, 25, 23, 00)),
            ('11.05 Show 11:00 PM', datetime(2010, 11, 05, 23, 00)),
            ('12.2 Show 11:00 PM', datetime(2010, 12, 2, 23, 00)),
            ('1.10 Show 11:00 PM', datetime(2011, 1, 10, 23, 00)),
            ('2.2 Show 11:00 PM', datetime(2011, 2, 2, 23, 00))
        ]
        
        
if __name__ == "__main__":
    unittest.main()
