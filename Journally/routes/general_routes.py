from flask import Blueprint, render_template
from flask_login import current_user, login_required, logout_user, login_user
from Journally import app
from Journally.models import User, Journal

general_bp = Blueprint("general", __name__)

@general_bp.route("/")
@general_bp.route("/home")
def home():
    return render_template("home.html")