from .storage.storage import get_station_by_index


class Route:
    def __init__(self, route):
        self.route = route
        self.directions = None

    def __hash__(self):
        return hash(''.join(self.route))

    def __eq__(self, other):
        if isinstance(other, Route):
            return self.route == other.route
        return False

    def __str__(self):
        return "Route: ({})\n".format(", ".join(get_station_by_index(index).get_code() for index in self.route)) \
               + "\n".join(self.__get_directions())

    @staticmethod
    def __get_direction(start, end):
        start = get_station_by_index(start)
        start_line = start.get_train_line()
        end = get_station_by_index(end)
        if start.get_train_line() == end.get_train_line():
            return "Take {} line from {} to {}".format(start_line, start.get_name(), end.get_name())
        else:
            return "Change from {} line to {} line".format(start_line, end.get_train_line())

    def __get_directions(self):
        if self.directions is not None:
            return self.directions
        if not self.route:
            return []

        self.directions = []
        start = self.route[0]
        for end in self.route[1:]:
            self.directions.append(Route.__get_direction(start, end))
            start = end
        return self.directions
