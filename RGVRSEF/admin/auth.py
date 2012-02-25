from hashlib import sha256

from flask import Blueprint, render_template, abort, request, url_for,\
                  flash, redirect
from flaskext.login import LoginManager, current_user, login_required,\
                           login_user, logout_user, AnonymousUser,\
                           confirm_login, fresh_login_required, UserMixin

from .. import app
from .models import Admin
from . import admin

class Anonymous(AnonymousUser):
    name = u"Anonymous"

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = ".login"
login_manager.login_message = u"Please log in to access this area"
login_manager.refresh_view = ".reauth"

@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id))

def check_login(username,password):
    user = Admin.query.filter_by(username=username).first()
    if username is not None: 
        if user.password == sha256(password).hexdigest():
            return user
    return None

login_manager.setup_app(app)

@admin.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        user = check_login(username,request.form.get("password",""))
        if user is not None:
            if login_user(user):
                return redirect(request.args.get("next") or url_for(".index"))
        else:
            flash("Sorry, your information did not match our records.")
    return render_template("admin/login.html")

@admin.route("/reauth", methods=["GET","POST"])
@login_required
def reauth():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        user = check_login(username,request.form.get("password",""))
        if user is not None:
            confirm_login()
            return redirect(request.args.get("next") or url_for(".index"))
        else:
            flash("Sorry, your information did not match our records.")
    return render_template("admin/login.html")

@admin.route("/logout")
@login_required
def logout():
    logout_user()
    #flash("Logged out.")
    return redirect(url_for("index"))

