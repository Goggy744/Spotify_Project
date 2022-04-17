# Imports : 
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .views import nav_user, nav_guest
from .models import Account
from . import db

# Creation of the authentification Blueprint
auth = Blueprint("auth", __name__)

# Creation of the first route : home route, register route
@auth.route("/", methods=["POST","GET"])
def home():
    # if method is post, we save username, pw and pw_confirmation + a possible account which already exist
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pw")
        pw_confirmation = request.form.get("pw-confirmation")
        existing_user = Account.query.filter_by(username=username).first()

        # if an account already exists with the same username => error message
        if existing_user:
            flash("Username already used", category="error")
            return render_template("base.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
        
        # if pw is not the same as pw-confirmation => error message
        elif password != pw_confirmation:
            flash("Password and Password Confirmation are not the same", category="error")
            return render_template("base.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
        
        # if username's lenght is below 3 => error message
        elif len(username) < 3:
            flash("Username must be more than 3 caracters", category="error")
            return render_template("base.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
        
        # else we create the account + hash the pw, add it to the db and log the user in the session + success message
        else:
            new_account = Account(username=username, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_account)
            db.session.commit()
            login_user(new_account, remember=True)
            flash("Your account has been registered", category="success")
            return redirect(url_for("auth.home"))

    # else we return the actual page without doing nothing
    else:
        return render_template("base.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
        


# Creation of the 2nd route : log in route, sign in route
@auth.route("/sign-in", methods=["POST", "GET"])
def sign_in():
    # if method = post: save the username + pw + search the account in the db
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pw")
        user = Account.query.filter_by(username=username).first()

        # if the account exists => check hashed pw
        if user:
            # if hashed pw is correct => log the user + success message
            if check_password_hash(user.password, password):
                flash("Logged In successfully", category="success")
                login_user(user)
                return redirect(url_for("auth.home"))
            # else error message about password 
            else:
                flash("Incorrect Password", category="error")
                return render_template("sign_in.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
        # else error message about username
        else:
            flash("Incorrect Username", category="error")
            return render_template("sign_in.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)
    # else return the page without doing nothing
    else:
        return render_template("sign_in.html", nav_guest=nav_guest, nav_user=nav_user, user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", category="success")
    return redirect(url_for("auth.home"))

