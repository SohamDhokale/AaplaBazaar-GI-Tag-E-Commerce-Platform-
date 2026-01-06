import os
import logging

from flask import Flask, request, session, url_for, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_babel import Babel


# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "aaplabazaar_secret_key")

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///aaplabazaar.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["BABEL_DEFAULT_LOCALE"] = "en"
app.config["BABEL_SUPPORTED_LOCALES"] = ["en", "hi", "mr"]

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

# initialize the app with the extension
db.init_app(app)

# Locale selector for Babel (Flask-Babel v3/4 style)
def get_locale():
    lang = request.args.get('lang') or session.get('lang')
    supported = app.config.get("BABEL_SUPPORTED_LOCALES", ["en"])
    if lang in supported:
        session['lang'] = lang
        g.current_lang = lang
        return lang
    best = request.accept_languages.best_match(supported)
    g.current_lang = best or supported[0]
    return g.current_lang

# Initialize Babel with the selector
babel = Babel(app, locale_selector=get_locale)

# Create a context processor to add variables to all templates
@app.context_processor
def inject_now():
    from datetime import datetime
    return {'now': datetime.utcnow()}

# Language helpers
@app.context_processor
def inject_language_tools():
    supported = app.config.get("BABEL_SUPPORTED_LOCALES", ["en"])
    # Ensure locale is resolved for this request
    current = get_locale()

    def build_lang_url(lang_code):
        args = request.args.to_dict()
        args['lang'] = lang_code
        view_args = request.view_args or {}
        endpoint = request.endpoint or 'index'
        try:
            return url_for(endpoint, **view_args, **args)
        except Exception:
            return url_for('index', lang=lang_code)

    from translations import translate
    return {
        'supported_languages': supported,
        'current_language': current,
        'build_lang_url': build_lang_url,
        't': lambda key, default=None: translate(current, key, default)
    }

# Import routes after initializing app to avoid circular imports
from routes import *

with app.app_context():
    # Import models here to ensure they're registered with SQLAlchemy
    import models
    db.create_all()
