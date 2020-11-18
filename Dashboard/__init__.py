from flask import Flask
import secrets

app = Flask(__name__)
secrect = secrets.token_urlsafe(32)
app.secret_key = secrect

from Dashboard import routes