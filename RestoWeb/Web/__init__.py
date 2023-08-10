from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from os import path
from flask_login import LoginManager
app = Flask(__name__)

csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///resto.db"
app.config['SECRET_KEY']='jaswanth'

db=SQLAlchemy(app)
login_manager=LoginManager(app)


from Web import views
