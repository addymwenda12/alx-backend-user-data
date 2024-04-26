#!/usr/bin/env python3
"""A simple Flask app with user authentication features.
"""

import bcrypt

from flask import Flask, jsonify, request, abort, make_response, redirect
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


def logout() -> str:
    """
    DELETE /sessions
    Return:
        - Redirect to GET / if the user is logged out successfully.
        - 403 HTTP status if the user does not exist.
    """
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    GET /profile
    Return:
        - JSON payload containing the user's email
        if the user is found.
        - 403 HTTP status if the session ID is invalid
        or the user does not exist.
    """
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    POST /reset_password
    Return:
        - JSON payload containing the user's email and reset token
        if the user is found.
        - 403 HTTP status if the email is not registered.
    """
    email = request.form.get('email')

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
