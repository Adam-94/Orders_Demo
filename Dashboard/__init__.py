from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from Dashboard.config import Config

import secrets

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
search = Search()
search.init_app(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from Dashboard.main.routes import main
from Dashboard.errors.handler import errors

app.register_blueprint(main)
app.register_blueprint(errors)