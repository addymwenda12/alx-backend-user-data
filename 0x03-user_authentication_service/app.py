#!/usr/bin/env python3
"""A simple Flask app with user authentication features.
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])


def welcome():
    """
    GET /
    Return:
        - JSON payload containing a welcome message.
    """
    return jsonify({"message": "Bienveneu"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
