#!/usr/bin/env python3
"""A simple Flask app with user authentication features.
"""

import bcrypt

from flask import Flask, jsonify, request, abort, make_response
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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    POST /sessions
    Return:
        - JSON payload containing a success message
        if the user is logged in successfully.
        - 401 HTTP status if the login information is incorrect.
    """
    email = request.form['email']
    password = request.form['password']

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(
            jsonify({"email": email, "message": "logged in"}), 200)
        response.set_cookie("session_id", session_id)
        return response

    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
