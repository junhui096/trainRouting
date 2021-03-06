from .stations_data import get_station_code_by_index, get_station_name_by_index, get_train_line_by_index

"""
Route class adds detailed directions to the list of station ids generated by the routing algorithm.
"""


class Route:

    @staticmethod
    def __get_directions(route, current_time):
        """
        Converts a sequence of station ids representing a route into a list of directions of steps to take.
        """
        def get_direction(start, end):
            start_line, end_line = get_train_line_by_index(start, None), get_train_line_by_index(end, None)

            start_name, end_name = get_station_name_by_index(start, None), get_station_name_by_index(end, None)
            if start_line == end_line:
                return "Take {} line from {} to {}".format(start_line, start_name, end_name)
            else:
                return "Change from {} line to {} line".format(start_line, end_line)

        directions = []
        start = route[0]
        for end in route[1:]:
            directions.append(get_direction(start, end))
            start = end
        return directions

    def __init__(self, route, start_time, end_time):
        self.route = route
        self.start_time = start_time
        self.end_time = end_time

    def __hash__(self):
        return hash(''.join(get_station_name_by_index(i, None) for i in self.route))

    def __eq__(self, other):
        """
        Two routes are equal if they share the same id sequence
        """
        if isinstance(other, Route):
            return [get_station_name_by_index(i, None) for i in self.route] == \
                   [get_station_name_by_index(i, None) for i in other.route]
        return False

    def __str__(self):
        """
        Returns detailed directions for travelling such as station code, and lines.
        """
        return "Route: ({})\n".format(
            ", ".join(get_station_code_by_index(index, None) for index in self.route)) \
               + "\n".join(Route.__get_directions(self.route, self.start_time))

    def num_stations(self):
        """
        Returns number of stations with distinct names(physical interchanges) in route.
        """
        return len({get_station_name_by_index(index, None) for index in self.route})

    def num_steps(self):
        """
        Returns number of steps(including transfers) in a route.
        """
        return len(self.route)

    def get_travel_time(self):
        """
        Returns number of minutes a route is expected to take.
        """
        return int((self.end_time - self.start_time).total_seconds() / 60)
