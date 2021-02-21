from . import storage
from datetime import datetime, timedelta

"""
This module will be invoked by other modules in the package. It provides a uniform layer of abstraction to query stations 
in the network. Stations can be queried by name or index(station_id). Methods return an index, abstracting out underlying representation of stations.
If current_time param is not specified (ie. None), all stations are returned. Otherwise, only stations that are currently open are returned
"""


def is_valid_station_name(name):
    """
    Returns True if station name is in storage.

            Parameters:
            name(str): name to verify

            Returns:
                    bool: True if valid else False
    """
    return name in storage.interchange_station_name_to_station_map


def get_station_ids_by_name(name, current_time):
    """
    Returns ids of all stations that are open and share same name.

            Parameters:
            name (string): name of station
            current_time(datetime): current time to check if stations are open

            Returns:
                    [int] ids of all stations.
    """
    if name not in storage.interchange_station_name_to_station_map:
        return []
    return storage.interchange_station_name_to_station_map[name].get_stations(current_time)


def __get_station_by_index(index, current_time):
    if index not in storage.station_index_to_station_map:
        return None
    station = storage.station_index_to_station_map[index]

    if not current_time or station.is_open(current_time):
        return station
    else:
        return None


def get_train_line_by_index(index, current_time):
    """
    Returns train line of corresponding station by index if station is open at current_time.

            Parameters:
            index (int): station id
            current_time(datetime): current time to check if stations are open

            Returns:
                    str?  train line
    """
    if not __get_station_by_index(index, current_time):
        return None
    return __get_station_by_index(index, current_time).get_train_line()


def get_station_code_by_index(index, current_time):
    """
    Returns code of station by index if open.

            Parameters:
            index (int): station id
            current_time(datetime): current time to check if stations are open

            Returns:
                   str? code of station
    """
    if not __get_station_by_index(index, current_time):
        return None
    return __get_station_by_index(index, current_time).get_code()


def get_station_name_by_index(index, current_time):
    """
    Returns name of station by index if open

            Parameters:
            index (int): station id
            current_time(datetime): current time to check if stations are open

            Returns:
                   str? name of station
    """
    if not __get_station_by_index(index, current_time):
        return None
    return __get_station_by_index(index, current_time).get_name()


def get_travel_time(source_id, dest_id, current_time):
    """
    Returns travel_time between stations by id from current_time.
    Assume that stations with source_id and dest_id are neighbours in network.

            Parameters:
            source_id (int): station id of starting station
            dest_id(int): station id of destination, neighbouring station.
            current_time(datetime): time of travel

            Returns:
                   datetime.timedelta time taken to travel between stations
            Raises:
                exception: Invalid source, dest_id or source station is not open at start of travel or dest station
                is not open at end of travel.
    """
    source = __get_station_by_index(source_id, current_time)
    dest = __get_station_by_index(dest_id, current_time)

    if not source:
        raise Exception("Invalid source_id")

    if not dest:
        raise Exception("Invalid dest_id")

    if not source.is_open(current_time):
        raise Exception("Station with id:{} is not open".format(source_id))

    if source_id == dest_id:
        return timedelta()

    travel_time = source.get_travel_time(dest, current_time)

    if not dest.is_open(current_time + travel_time):
        raise Exception("Station with id:{} is not open".format(dest_id))

    return travel_time
