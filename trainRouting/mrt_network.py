from .storage.storage import get_station_by_index
from datetime import date
from .route import Route


class MRTNetwork:
    def __init__(self, stations):
        self.network = stations

    @staticmethod
    def get_all_routes(source, dest, current_date=date.today()):
        visited = {source}
        routes = set()

        def dfs(node, route):
            if node == dest:
                routes.add(Route([i for i in route]))
                return
            for adj_node in get_station_by_index(node).get_neighbours(current_date):
                if adj_node not in visited:
                    visited.add(adj_node)
                    route.append(adj_node)
                    dfs(adj_node, route)
                    visited.remove(adj_node)
                    route.pop()

        if source == dest:
            return []
        else:
            dfs(source, [source])
        return routes
