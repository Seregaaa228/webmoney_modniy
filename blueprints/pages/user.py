from flask import Blueprint, render_template, jsonify, session
from flask_login import login_required
from blueprints import deps

pages_blueprint = Blueprint("pages_blueprint", __name__, url_prefix="/pages")


@pages_blueprint.route("/profile/", methods=["GET"])
@login_required
def cabinet():
    user = deps.get_user_by_id(session.get('_user_id'))
    return render_template("personal-cabinet.html", name=user[1])
