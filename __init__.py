from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

BASEDIR = Path(__file__).parents[1]
app = Flask(__name__, static_folder=BASEDIR / 'images')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Secret key'

db = SQLAlchemy(app)

from . import models, views

db.create_all()
