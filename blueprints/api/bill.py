from flask import Blueprint, jsonify, redirect, request, session
from flask_login import login_required

from blueprints import deps
from core.db import get_connection
from crud import bill_crud, user_crud

bill_blueprint = Blueprint('bill_blueprint', __name__, url_prefix="/bill")


@login_required
@bill_blueprint.route("/", methods=["POST"])
def create_bill():
    with get_connection() as conn:
        user = deps.get_user_by_id(session.get('_user_id'))
        bill_crud.create(conn, user[0])
        user_crud.new_bill(conn, user[1])
    return redirect("/success/")


@login_required
@bill_blueprint.route("/delete/<string:bill_id>", methods=["POST"])
def unact(bill_id):
    with get_connection() as conn:
        bill_crud.get_unactive(conn, bill_id)
        user_crud.restore_balance(conn, session.get("_user_id"))

    return redirect("/success")


@login_required
@bill_blueprint.route("/add/<string:bill_id>/<int:money>")
def add(bill_id, money):
    with get_connection() as conn:
        bill = bill_crud.get(conn, bill_id)
        login = user_crud.get_login_by_id(conn, bill.owner)
        bill_crud.add_money(conn, money, bill.balance, bill_id)
        user_crud.restore_balance(conn,bill_crud.get(conn,bill_id).owner)

        print(bill.owner, bill.balance, login, " - added")
        return redirect("/success/")


@login_required
@bill_blueprint.route("/add", methods=["POST"])
def redir_add():
    sender_id = request.form.get("sender_bill_id")
    money = request.form.get("money")
    return redirect(f"/bill/add/{sender_id}/{int(money)}")


