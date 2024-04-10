#!/usr/bin/env python3
"""
Flask app setup
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _


app = Flask(__name__, template_folder='templates')
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
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
    welcome_message = _('not_logged_in')
    if g.user:
        welcome_message = _('logged_in_as', username=g.user['name'])
    return render_template('5-index.html', welcome_message=welcome_message)


@babel.localeselector
def get_locale() -> str:
    """
    determines the bestbmatch in supported languages
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user(user_id) -> dict:
    """
    returns user dictionary or none if id not found in user
    """
    return users.get(user_id)


@app.before_request
def before_request():
    user_id = request.args.get('login_as', type=int)
    g.user = get_user(user_id)


if __name__ == '__main__':
    """
    the main
    """
    app.run(debug=True)
