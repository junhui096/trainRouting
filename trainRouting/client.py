from datetime import datetime
from .mrt_network import MRTNetwork
from .stations_data import get_station_ids_by_name, is_valid_station_name
from . import config


def get_all_routes(source, dest, current_time=config.DEFAULT_DATE_TIME, use_time_costs=False):
    """
    Driver function to be invoked by package client. Calls the routing algorithm (mrt_network.py), retrieves the routes,
     and returns its details to client of package.

            Parameters:
                    source (string): name of source station
                    dest (string): name of dest station
                    current_time(datetime): expected route start time
                    use_time_costs(bool): True if time between stations is factored into routing

            Returns:
                    list[dict]: A list of dictionaries for each route. Each dictionary has two fields: The first field Info
                    gives a summary of the route, while the second field Route gives detailed directions.
    """
    if source == dest:
        return []

    if not(is_valid_station_name(source)):
        raise Exception("Invalid source station name {}".format(source))

    if not (is_valid_station_name(dest)):
        raise Exception("Invalid dest station name {}".format(dest))

    source_ids = get_station_ids_by_name(source, current_time)
    dest_ids = get_station_ids_by_name(dest, current_time=None)

    if not source_ids:
        return []
    if not dest_ids:
        raise Exception("Invalid name for destination station")

    all_routes = set()
    for source_index in source_ids:
        for dest_index in dest_ids:
            for route in MRTNetwork.get_routes(source_index, dest_index, current_time, use_time_costs):
                all_routes.add(route)

    if use_time_costs:
        all_routes = sorted([i for i in all_routes], key=lambda rt: (rt.get_travel_time(), rt.num_stations(),
                                                                     rt.num_steps()))
    else:
        all_routes = sorted([i for i in all_routes], key=lambda rt: (rt.num_stations(), rt.num_steps()))

    if use_time_costs:
        return [{"Info": str(rt.get_travel_time()), "Route": str(rt)} for rt in all_routes]

    return [{"Info": str(rt.num_stations()), "Route": str(rt)} for rt in all_routes]