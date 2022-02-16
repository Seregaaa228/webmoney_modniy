from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required

from blueprints import deps
from core import passwords
from models.user import RegistrationModel, AuthUserModel
from core.db import get_connection
from crud import user_crud
from models.user_login import UserLogin

auth_blueprint = Blueprint('auth_blueprint', __name__, url_prefix='/auth')


@auth_blueprint.route('/login')
def login():
    return render_template('login.html')


@auth_blueprint.route('/signup')
def signup():
    return render_template('signup.html')


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('api_blueprint.auth_blueprint.login'))


@auth_blueprint.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    password = request.form.get('password')
    registration_data = RegistrationModel(login=name, password=password)

    with get_connection() as conn:
        user = user_crud.get(conn, name)
        UserLogin().create(user)
        if user is not None:
            flash(f"User with login {name} already exist")
        elif " " in name:
            flash("No spaces allowed in login")
            return redirect(url_for("api_blueprint.auth_blueprint.signup"))
        else:
            user_crud.create(conn, registration_data)
            flash("Пользователь создан, теперь войдите")

    return redirect(url_for('api_blueprint.auth_blueprint.login'))


@auth_blueprint.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')
    auth_data = AuthUserModel(username=name, password=password)

    with get_connection() as conn:
        user = user_crud.get(conn, name)

        if user_crud.authenticate(conn, auth_data) is None:
            flash("User does not exist")
            return redirect(url_for("api_blueprint.auth_blueprint.login"))
        if not passwords.passwords_equal(auth_data.password, user_crud.get(conn, auth_data.username)[4]):
            flash("Password is incorrect")
            return redirect(url_for("api_blueprint.auth_blueprint.login"))
        if auth_data.username == "":
            flash("Field name must be filled")
            return redirect(url_for("api_blueprint.auth_blueprint.login"))
        userLogin = UserLogin().create(user)
        login_user(userLogin)

    return redirect(f"/pages/profile/")
