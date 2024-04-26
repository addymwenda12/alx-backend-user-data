#!/usr/bin/env python3
"""
This defines the User model for the database
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User class that representsa user in the database

    Attributes:
        id (Integer): The user id
        email (String): The user email
        hashed_password (String): The user hashed password
        session_id (String)": The user session id
        reset_token (String): The user reset token
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
