from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

import secrets

app = Flask(__name__)
secret = secrets.token_urlsafe(32)
app.config['SECRET_KEY'] = secret
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['TESTING'] = True

db = SQLAlchemy(app)
search = Search()
search.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'



from Dashboard import routes