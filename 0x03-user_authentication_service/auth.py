#!/usr/bin/env python3
"""
This module contains the Auth class which provides authentication
for the user
"""

import bcrypt

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """
    Hash a password with bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a user.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the password matches with the hashed password stored for the user, False otherwise.
        """
        user = self._db.find_user_by(email=email)  # Assuming _db is a database instance with a method find_user_by
        if user:
            hashed_password = user.password  # Assuming the user object has a password attribute
            return bcrypt.checkpw(password.encode(), hashed_password.encode())
        return False
