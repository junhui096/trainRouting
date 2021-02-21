import pandas as pd
from . import stations
from datetime import datetime
from .. import config

"""
Loads csv file and retrieves details of all stations into a map.
"""


def load_csv(file_path=config.STATION_FILE_PATH):
    """
    Loads csv file

            Parameters:
            file_path: file location as set in config.py

            Returns:
                   map, map: mapping of station name to interchange station model, mapping of station id to inner stations model.
    """

    interchange_station_name_to_station_map = {}
    station_index_to_station_map = {}

    try:
        df = pd.read_csv(file_path)
    except IOError:
        print("The csv file cannot be found. Set STATION_FILE_PATH variable with the csv file location in config.py")
        return interchange_station_name_to_station_map, station_index_to_station_map

    for index, row in df.iterrows():
        try:
            opening_date = datetime.strptime(row['Opening Date'], '%d-%b-%y').date()
        except ValueError:
            opening_date = datetime.strptime(row['Opening Date'], '%b-%y').date()

        name = row['Station Name']
        if name not in interchange_station_name_to_station_map:
            st = stations.InterchangeStation(name=name)
            interchange_station_name_to_station_map[st.name] = st
        else:
            st = interchange_station_name_to_station_map[name]

        station_index_to_station_map[index] = st.add_station(station_id=index, code=row['Station Code'],
                                                             opening_date=opening_date)
    return interchange_station_name_to_station_map, station_index_to_station_map


interchange_station_name_to_station_map, station_index_to_station_map = load_csv()
