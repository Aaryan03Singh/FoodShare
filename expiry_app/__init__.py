from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'AARYAN'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
UPLOAD_FOLDER = 'expiry_app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


   

db= SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view= 'login'
login_manager.login_message_category = 'info'

from expiry_app import routes