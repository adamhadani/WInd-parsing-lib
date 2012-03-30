#!/usr/bin/env python
"""Custom exception types used by framework"""
 
class ParsingFailed(Exception):
    """Raised when a parsing error,
    e.g for schema matching, occurs"""
