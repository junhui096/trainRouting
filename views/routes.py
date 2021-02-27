from flask import Blueprint, request
from datetime import datetime
from .. import templates
from ..trainRouting import get_all_routes

routes = Blueprint('routes', __name__)

"""
GET request handler. Parses URL request for source, end, and start_time parameters. 
Invokes train routing client package with these fields to obtain routes to be rendered by templates.
"""


@routes.route("/api/v1/get_routes")
def get_routes():
    try:
        source = request.args.get("start")
        if not source:
            return "Missing start query parameter", 400
        source = str(source)
    except:
        return "Cannot decode start query parameter", 400

    try:
        dest = request.args.get("end")
        if not dest:
            return "Missing end query parameter", 400
        dest = str(dest)
    except:
        return "Cannot decode end query parameter", 400

    if source == dest:
        return "The start and end stations cannot be the same.", 400

    start_time = request.args.get("start_time")
    if not start_time:
        use_time_costs = False
        start_time = datetime.min
    else:
        use_time_costs = True
        try:
            start_time = datetime.strptime(start_time.strip(), "%Y-%m-%dT%H:%M")
        except Exception as e:
            return "Invalid start time " + str(e), 400

    try:
        routes = get_all_routes(source, dest, start_time, use_time_costs)
        response = templates.build_response(source, dest, routes, use_time_costs)
        print(response.replace("<br/>", "\n"))
        return response, 200

    except Exception as e:
        return "Error finding routes. Ensure the name of start and end stations are valid.", 404

