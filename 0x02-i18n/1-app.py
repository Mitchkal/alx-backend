#!/usr/bin/env python3
"""
Flask app setup
"""
from flask import Flask, render_template
from flask_babel import Babel


app = Flask(__name__, template_folder='templates')
babel = Babel(app)


class Config:
    """
    babel configuration
    for languages
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """
    index function to render template
    """
    return render_template('0-index.html')


if __name__ == '__main__':
    """
    the main
    """
    app.run(debug=True)
