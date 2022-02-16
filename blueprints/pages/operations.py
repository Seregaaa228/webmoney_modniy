from flask import Blueprint, render_template, session
from flask_login import login_required

from blueprints import deps
from crud import user_crud
from core.db import get_connection

operations_blueprint = Blueprint("operations_blueprint", __name__)


@login_required
@operations_blueprint.route('/pages/add/')
def add_form():
    with get_connection() as conn:
        bill_active = []
        user = deps.get_user_by_id(session.get('_user_id'))
        bills = user_crud.get_all_bills(conn, user[0])


    return render_template("add.html", bills=bills, name=user[1])


@login_required
@operations_blueprint.route("/pages/transfer/")
def transfer():
    with get_connection() as conn:
        user = deps.get_user_by_id(session.get('_user_id'))
        bills = user_crud.get_all_bills(conn, user[0])
    return render_template("transfer.html", bills=bills, name=user[1])


@login_required
@operations_blueprint.route("/success/")
def success():
    user = deps.get_user_by_id(session.get('_user_id'))
    return render_template("success.html", name=user[1])
