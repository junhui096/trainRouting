import re
from .cost_calculator import CostCalculatorFactory

"""
Represents each of the train platforms with a distinct ID.  Multiple stations can have same name.
"""


class Station:
    def __init__(self, station_id, code, name, opening_date):
        parsed_station_code = re.match(r"([A-Za-z]+)(\d+)", code.strip())
        self.station_line = parsed_station_code.group(1)
        self.cost_calculator = CostCalculatorFactory.create(self.station_line)
        self.station_id = station_id
        self.code = code
        self.name = name.strip()
        self.opening_date = opening_date

    def is_open(self, current_time):
        """
        Returns true if station is open at current_time.
        """
        return current_time.date() >= self.opening_date and self.cost_calculator.is_open(current_time)

    def get_code(self):
        """
        Getter for station code. E.g EW11
        """
        return self.code

    def get_name(self):
        """
        Getter of station name. E.g. Jurong East
        """
        return self.name

    def get_train_line(self):
        """
        Getter of train line. E.g. CC, DT
        """
        return self.station_line

    def get_travel_time(self, dest, current_time):
        """
        Returns time needed to travel between current station and dest station at current time
        """
        if self.get_train_line() == dest.get_train_line():
            return self.cost_calculator.get_travel_cost_per_station(current_time)
        else:
            return self.cost_calculator.get_transfer_costs(current_time)


"""
Models a physical train station under the same distinct name, comprising of different inner stations with their own station codes.
"""


class InterchangeStation:
    def __init__(self, name):
        self.name = name.strip()
        self.stations = []
        if not name:
            raise Exception("name field is empty")

    def add_station(self, station_id, code, opening_date):
        """
        Adds a station to a physical interchange station.
        """
        st = Station(station_id=station_id, code=code, name=self.name, opening_date=opening_date)
        self.stations.append(st)
        return st

    def get_stations(self, current_time):
        """
        Getter of all stations with the same name.
        """
        if not current_time:
            return [st.station_id for st in self.stations]

        return [st.station_id for st in self.stations if st.is_open(current_time)]
