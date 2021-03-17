from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import pymysql

# Local Modules
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

pymysql.install_as_MySQLdb()  # FIX: Error No module named MySQLdb

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login'


from app import views, models  # This should remain at the bottom file.
