import re
from datetime import date
from . import storage


class Station:
    def __init__(self, station_id, code, name, opening_date):
        self.parsed_station_code = re.match(r"([A-Za-z]+)(\d+)", code.strip())
        self.station_id = station_id
        self.code = code
        self.name = name.strip()
        self.opening_date = opening_date

    def is_open(self, current_date=date.today()):
        return current_date >= self.opening_date

    def get_code(self):
        return self.code

    def get_name(self):
        return self.name

    def get_train_line(self):
        return self.parsed_station_code.group(1)

    def get_neighbours(self, current_date=date.today()):
        neighbours = {i for i in storage.get_station_by_name(self.name).get_stations(current_date)}
        for index in [self.station_id - 1, self.station_id + 1]:
            neigh = storage.get_station_by_index(index)
            if neigh and neigh.is_open(current_date) and neigh.get_train_line() == self.get_train_line():
                neighbours.add(index)

        neighbours.remove(self.station_id)
        return neighbours


class InterchangeStation:
    def __init__(self, name):
        self.name = name.strip()
        self.stations = []
        if not name:
            raise Exception("name field is empty")

    def add_station(self, station_id, code, opening_date):
        st = Station(station_id=station_id, code=code, name=self.name, opening_date=opening_date)
        self.stations.append(st)
        return st

    def get_stations(self, current_date=date.today()):
        return [st.station_id for st in self.stations if st.is_open(current_date)]
