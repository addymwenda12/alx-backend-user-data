#!/usr/bin/env python3
"""
Module for filtering log messages
"""

import re
import logging
from typing import List, Tuple

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
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


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class.

    This class extends the logging.Formatter class to support log message
    redaction. It replaces specified fields in the log messages with a
    redaction string to prevent sensitive information from being logged.

    Attributes:
        fields (List[str]): A list of field names to obfuscate.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize RedactingFormatter with the fields to obfuscate.

        Args:
            fields (List[str]): A list of field names to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified log record and obfuscate specified fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record with specified fields obfuscated.
        """
        original_message = logging.Formatter.format(self, record)
        return filter_datum(self.fields,
                            self.REDACTION, original_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object.

    The logger is named "user_data", logs up to logging.INFO level,
    does not propagate messages to other loggers,
    and has a StreamHandler with RedactingFormatter as formatter.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger
