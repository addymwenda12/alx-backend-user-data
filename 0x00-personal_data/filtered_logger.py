#!/usr/bin/env python3
"""
Module for filtering log messages
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscate specific fields in a log message.

    Parameters:
    fields (list): A list of strings representing all fields to obfuscate.
    redaction (str): A string representing by what the field
    will be obfuscated.
    message (str): A string representing the log line.
    separator (str): A string representing by which character is
    separating all fields in the log line.

    Returns:
    str: The log message with obfuscated fields.
    """
    regex = re.compile(r'({})=(.*?)(?={})'.format('|'.join(fields), separator))
    return regex.sub(r'\2={}{}'.format(redaction, separator), message)
