#!/usr/bin/env python3
"""
Module for filtering log messages
"""

import re
from typing import List, Tuple


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Returns the log message with the specified fields obfuscated.

    :param fields: List of field names to obfuscate
    :param redaction: String to replace the field values with
    :param message: Log message as a string
    :param separator: Character separating fields in the log message
    :return: Log message with obfuscated fields
    """
    for field in fields:
        message = re.sub(fr'{field}=(.*?);', f'{field}={redaction};', message)
    return message
