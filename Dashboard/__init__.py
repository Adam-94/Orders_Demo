from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from Dashboard.config import Config


db = SQLAlchemy()
search = Search()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "main.login"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    search.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from Dashboard.main.routes import main
    from Dashboard.errors.handler import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
