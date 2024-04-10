#!/usr/bin/env python3
"""
Flask app setup
"""
import pytz
from datetime import datetime
from flask import Flask, render_template, request, g
from flask_babel import Babel, _, timezone, format_datetime
from typing import Union


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
    time_zone = get_timezone()
    _timezone = pytz.timezone(time_zone)
    complete_time = datetime.now(_timezone)

    current_time_f = format_datetime(datetime=complete_time)

    welcome_message = _('not_logged_in')
    if g.user:
        welcome_message = _('logged_in_as', username=g.user['name'])
    return render_template('index.html', welcome_message=welcome_message,
                           current_time_is=current_time_f)


@babel.localeselector
def get_locale() -> str:
    """
    determines the bestbmatch in supported languages
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    user_locale = g.user.get('locale') if g.user else None
    if user_locale in app.config['LANGUAGES']:
        return user_locale

    best_match = request.accept_languages.best_match(app.config['LANGUAGES'])
    if best_match:
        return best_match

    return app.config['BABEL_DEFAULT_LOCALE']


def get_user(user_id) -> Union[dict, None]:
    """
    returns user dictionary or none if id not found in user
    """
    if user_id is not None:
        return users.get(user_id)
    return None


@app.before_request
def before_request():
    """
    runs before the request to retrieve user id
    """
    user_id = request.args.get('login_as', type=int)
    g.user = get_user(user_id)


@babel.timezoneselector
def get_timezone() -> str:
    """
    determines the best matching timezone
    """
    timezone_param = request.args.get('timezone')
    if timezone_param:
        try:
            pyt.timezone(timezone_param)
            return timezone_param
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    if g.user and g.user.get('timezone'):
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    return app.config['BABEL_DEFAULT_TIMEZONE']


if __name__ == '__main__':
    """
    the main
    """
    app.run(debug=True)
