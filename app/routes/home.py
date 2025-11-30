from flask import Blueprint, render_template

home_bp = Blueprint('main', __name__)

@home_bp.route("/")
def home():
    return render_template("index.html", title="Home")