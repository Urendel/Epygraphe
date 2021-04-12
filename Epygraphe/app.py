from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from warnings import warn
from .reglages import SECRET_KEY
import os


path = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(path, "templates")
statics = os.path.join(path, "static")
data = os.path.join(path, "data")
database = os.path.join(data, "epygraphe_bdd.sqlite")


if SECRET_KEY == "CLEF A CHANGER":
    warn("Il est conseillé de changer la clef de cryptage", Warning)

app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics
)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login = LoginManager(app)

from .routes import routes