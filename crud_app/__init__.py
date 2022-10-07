from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://test.db"
app.config['SECRET_KEY'] = 'a9989de36247ea226d7bd1f0'

db = SQLAlchemy(app) #initalizing database

from crud_app import routes
