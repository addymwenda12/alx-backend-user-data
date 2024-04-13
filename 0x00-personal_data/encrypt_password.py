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
