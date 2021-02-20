from datetime import datetime
from .mrt_network import MRTNetwork
from .storage import get_station_by_name


def get_all_routes(source, dest, current_time=datetime.now(), order_by=""):
    if source == dest:
        return []

    source = get_station_by_name(source)
    dest = get_station_by_name(dest)

    if not source:
        raise Exception("Invalid name for starting station")
    if not dest:
        raise Exception("Invalid name for destination station")

    all_routes = set()
    for source_index in source.get_stations(current_time.date()):
        for dest_index in dest.get_stations(current_time.date()):
            for route in MRTNetwork.get_routes(source_index, dest_index, current_time):
                all_routes.add(route)

    if not order_by:
        all_routes = sorted([i for i in all_routes], key=lambda rt: (rt.num_stations(), rt.num_steps()))

    return [(str(rt), rt.num_stations) for rt in all_routes]