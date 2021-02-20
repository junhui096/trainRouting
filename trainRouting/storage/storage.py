import pandas as pd
from trainRouting import stations

from datetime import datetime

df = pd.read_csv('StationMap.csv')

interchange_station_name_to_station_map = {}
station_index_to_station_map = {}

for index, row in df.iterrows():
    opening_date = datetime.strptime(row['Opening Date'], '%d-%b-%y').date()
    name = row['Station Name']
    if name not in interchange_station_name_to_station_map:
        st = stations.InterchangeStation(name=name)
        interchange_station_name_to_station_map[st.name] = st
    else:
        st = interchange_station_name_to_station_map[name]

    station_index_to_station_map[index] = st.add_station(station_id=index, code=row['Station Code'],
                                                         opening_date=opening_date)


def get_station_by_index(index):
    if index not in station_index_to_station_map:
        return None
    return station_index_to_station_map[index]


def get_station_by_name(name):
    if name not in interchange_station_name_to_station_map:
        return None
    return interchange_station_name_to_station_map[name]
