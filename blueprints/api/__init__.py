from flask import Blueprint, jsonify

from .index import index_blueprint
from .user import user_blueprint
from .bill import bill_blueprint
from .auth import auth_blueprint
from pydantic import ValidationError
from blueprints.pages.user import pages_blueprint
from blueprints.pages.operations import operations_blueprint
from werkzeug.exceptions import HTTPException

api_blueprint = Blueprint("api_blueprint", __name__, url_prefix="")
api_blueprint.register_blueprint(user_blueprint)
api_blueprint.register_blueprint(bill_blueprint)
api_blueprint.register_blueprint(auth_blueprint)
api_blueprint.register_blueprint(index_blueprint)
api_blueprint.register_blueprint(pages_blueprint)
api_blueprint.register_blueprint(operations_blueprint)

@api_blueprint.errorhandler(ValidationError)
def register_validation_error(error: ValidationError):
    return jsonify({"error": type(error).__name__, "info": error.errors()}), 422


@api_blueprint.errorhandler(HTTPException)
def register_default_error(error: HTTPException):
    return (
        jsonify({"error": type(error).__name__, "info": error.description}),
        error.code,
    )