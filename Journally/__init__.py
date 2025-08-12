from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SKIBIDI TOILET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

from Journally.routes.general_routes import general_bp
from Journally.routes.auth_routes import auth_bp

app.register_blueprint(general_bp)
app.register_blueprint(auth_bp)