#!/usr/bin/env python3
"""
Flask app setup
"""
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index() -> str:
    """
    index function to render template
    """
    return render_template('index.html')


if __name__ == '__main__':
    """
    the main
    """
    app.run(debug=True)
