# .../api/user
from typing import Any

from flask import Blueprint, jsonify, redirect, request, session, render_template, flash, url_for
from flask_login import login_required

from crud import user_crud, bill_crud
from core.db import get_connection
from core import passwords

user_blueprint = Blueprint("user_blueprint", __name__, url_prefix="/user")


@login_required
@user_blueprint.route("/transfer/<string:bill_id_sender>/<string:receiver_bill_id>/<int:money>", methods=["GET"])
def transfer(bill_id_sender: str, receiver_bill_id: str, money: int):
    with get_connection() as conn:
        bill_crud.transfer_money(conn, sender_bill_id=bill_id_sender, receiver_bill_id=receiver_bill_id, money=money)
        user_crud.restore_balance(conn, bill_crud.get(conn, bill_id_sender).owner)
        user_crud.restore_balance(conn, bill_crud.get(conn, receiver_bill_id).owner)
    return redirect("/success/")


@login_required
@user_blueprint.route('/about/')
def about_user():
    with get_connection() as conn:
        user = user_crud.getbyId(conn, session.get('_user_id'))
        user_crud.restore_balance(conn, session.get("_user_id"))
        return render_template("about.html", id=user[0], login=user[1], balance=user[3])


@user_blueprint.route("/transaction/")
def get_transact():
    with get_connection() as conn:
        data = user_crud.get_user_transactions(conn, session.get('_user_id'))
        return render_template("transactions.html", bills=data)


@login_required
@user_blueprint.route("/transfer/", methods=["POST"])
def redir_transfer():
    sender_id = request.form.get("sender_bill_id")
    money = request.form.get("money")
    receiver = request.form.get("receiver")
    return redirect(f"/user/transfer/{sender_id}/{receiver}/{int(money)}")


@login_required
@user_blueprint.route("/change-password/")
def change_password_plate():
    return render_template('change-password.html')


@login_required
@user_blueprint.route("/change-password/", methods=['POST'])
def change_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    with get_connection() as conn:
        user = user_crud.getbyId(conn, session.get("_user_id"))
        if not passwords.passwords_equal(old_password, user[4]):
            flash("Incorrect password")
            return render_template("change-password.html")
        if old_password == new_password:
            flash("Same password")
            return render_template("change-password.html")

        user_crud.get_user_password_change(conn, user[0], new_password)
    return redirect(url_for('api_blueprint.auth_blueprint.logout'))


@login_required
@user_blueprint.route("/delete-user/")
def delete_user_plate():
    return render_template("delete-user.html")


@login_required
@user_blueprint.route("/delete-user/", methods=['POST'])
def delete_user():
    password = request.form.get("password")
    with get_connection() as conn:
        user = user_crud.getbyId(conn, session.get("_user_id"))
        if not passwords.passwords_equal(password, user[4]):
            flash("Incorrect password")
            return render_template("delete-user.html")
        if user_crud.get_all_bills(conn, user[0]) is not None:
            bill_crud.delete_bills(conn, user[0])
        user_crud.delete_user(conn, user[0])
    return redirect("/")


@login_required
@user_blueprint.route("/get-bills/")
def get_bills():
    with get_connection() as conn:
        return render_template("bills.html", bills=bill_crud.get_bills(conn, session.get("_user_id")))
