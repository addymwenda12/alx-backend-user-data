#!/usr/bin/env python3
"""A simple Flask app with user authentication features.
"""

import bcrypt

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """
    GET /
    Return:
        - JSON payload containing a welcome message.
    """
    return jsonify({"message": "Bienveneu"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
    POST /users
    Return:
        - JSON payload containing a success message
        if the user is registered successfully.
        - JSON payload containing an error message
        if the user is already registered.
    """
    email = request.form['email']
    password = request.form['password']

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


class Auth:
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")