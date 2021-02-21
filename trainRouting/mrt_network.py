from .stations_data import get_station_ids_by_name, get_travel_time, get_station_name_by_index, get_train_line_by_index
from .route import Route
from collections import deque, defaultdict
import heapq
from datetime import datetime, timedelta

"""
The MRT network is modelled as a graph, with each Node representing a station code in the network.
"""


class MRTNetwork:
    class Node:
        """
        A Node encapsulates a state in a route comprising of the current location, given by the station id, the current time
        and the preceding state, denoted by the parent field.
        """
        def __init__(self, station_id, current_time, parent=None):
            self.station_id = station_id
            self.current_time = current_time
            self.parent = parent

        def get_id(self):
            """
            Returns id of station corresponding to location of current node.
            """
            return self.station_id

        def get_current_time(self):
            """
            Getter for time field of current node.
            """
            return self.current_time

        def get_parent(self):
            """
            Gets preceding node in route.
            """
            return self.parent

        """
        Nodes are ordered first by their current time, second by their id in heap.
        """

        def __lt__(self, other):
            return (self.current_time, self.get_id()) < (other.get_current_time(), other.get_id())

        def __gt__(self, other):
            return (self.current_time, self.get_id()) > (other.get_current_time(), other.get_id())

        def get_neighbours(self, use_time_costs=False):
            """
            Returns all nodes that are adjacent in the train network to self. These nodes are either on the same train line
            with consecutive IDs, or belong to the same physical interchange station.

                    Parameters:
                            use_time_costs(bool): True if time to travel between MRT stations(nodes) is factored into computing
                            min cost route.

                    Returns:
                            {Node}: Set of adj nodes
            """
            neighbours_ids = set()
            neighbours = set()
            train_line = get_train_line_by_index(self.station_id, self.current_time)
            station_ids = get_station_ids_by_name(get_station_name_by_index(self.station_id,
                                                                            self.current_time),
                                                  self.current_time)
            cost_generator = lambda neigh_id: timedelta(minutes=1)
            if use_time_costs:
                cost_generator = lambda neigh_id: get_travel_time(source_id=self.station_id, dest_id=neigh_id,
                                                                  current_time=self.current_time)

            for station_id in station_ids:
                neighbours_ids.add(station_id)
            for index in [-1, 1]:
                neigh_id = self.station_id + index
                try:
                    neigh_line = get_train_line_by_index(neigh_id, self.current_time + cost_generator(neigh_id))
                except:
                    continue

                if neigh_line and neigh_line == train_line:
                    neighbours_ids.add(neigh_id)

            if self.station_id in neighbours_ids:
                neighbours_ids.remove(self.station_id)
            for i in neighbours_ids:
                try:
                    node = MRTNetwork.Node(i, self.current_time + cost_generator(i), parent=self)
                    neighbours.add(node)
                except:
                    pass
            return neighbours

    @staticmethod
    def __get_route(source, dest, current_time, use_time_costs):
        """
        Djikstra algorithm implementation to find min cost route from source to dest from current_time
        """
        source_node = MRTNetwork.Node(source, current_time)
        visited = set()
        end_times = defaultdict(lambda: datetime.max)
        nodes = [source_node]
        while nodes:
            node = heapq.heappop(nodes)

            if node.get_id() == dest:
                return node
            if node.get_id() in visited:
                continue
            visited.add(node.get_id())
            neighbours = node.get_neighbours(use_time_costs)

            for neighbour in neighbours:
                if neighbour.get_id() in visited or neighbour.get_current_time() >= end_times[neighbour.get_id()]:
                    continue
                else:
                    end_times[neighbour.get_id()] = neighbour.get_current_time()
                    heapq.heappush(nodes, neighbour)
        return None

    @staticmethod
    def get_routes(source, dest, current_time, use_time_costs):
        """
        Returns shortest route between source and destination station, where shortest can be in terms of number of
        stations traversed or earliest end time.

                Parameters:
                        source (string): name of source station
                        dest (string): name of dest station
                        current_time(datetime): expected route start time
                        use_time_costs(bool): True if time to travel between MRT stations(nodes) is factored into computing
                        min cost route.

                Returns:
                        list[Route]: A list of routes of least cost from source to dest or
                        an empty list if dest is unreachable from source.
        """
        if source == dest:
            return []
        last_node = MRTNetwork.__get_route(source, dest, current_time, use_time_costs)
        if not last_node:
            return []
        end_time = last_node.get_current_time()

        route = deque()
        while last_node:
            route.appendleft(last_node)
            last_node = last_node.get_parent()
        return [Route([i.get_id() for i in route], start_time=current_time, end_time=end_time)]
