from flask import Blueprint

routes = Blueprint('routes', __name__)


@routes.route("/")
def get_routes():
    return "Hello World"
