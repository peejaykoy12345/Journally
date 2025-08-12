from flask import Blueprint, render_template
from Journally import app

general_bp = Blueprint("general", __name__)

@general_bp.route("/")
@general_bp.route("/home")
def home():
    return render_template("home.html")