from flask import Blueprint, render_template


auth = Blueprint("auth", __name__)


@auth.route("/sign-up")
def sign_up():
    pass


@auth.route("/sign-in")
def sign_in():
    pass