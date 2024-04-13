#!/usr/bin/env python3
"""
Module for encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with a randomly-generated salt and
    returns the hashed password.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the
    hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
