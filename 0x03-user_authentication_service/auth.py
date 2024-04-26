#!/usr/bin/env python3
"""
This module contains the Auth class which provides authentication
for the user
"""

import bcrypt
import uuid

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


def _generate_uuid() -> str:
    """
    Generate a new UUID

    Returns:
        str: The string representation of the new UUID.
    """
    return str(uuid.uuid4())


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
            bool: True if the password matches with the hashed password
            stored for the user, False otherwise.
        """
        user = self._db.find_user_by(email=email)
        if user:
            hashed_password = user.password
            return bcrypt.checkpw(password.encode(), hashed_password.encode())
        return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for a user

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID if the user exists, None otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str):
        """
        Get the user corresponding to a session ID

        Args:
            session_id (str): The session ID.

        Returns:
            User: The user corresponding to the session ID
            if the user exists, None otherwise.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session

        Args:
            user_id (int): The user's ID.

        Returns:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Get a reset password token for a user

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset password token if the user exists.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = str(uuid.uuid4())
            self._db.update_user(user.id, reset_token=reset_token)

            return reset_token
        except Exception:
            raise ValueError("User does not exist")
