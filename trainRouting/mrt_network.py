from .storage import get_station_by_index
from .route import Route


class MRTNetwork:

    @staticmethod
    def get_routes(source, dest, current_time):
        visited = {source}
        routes = set()

        def dfs(node, route):
            print(node, source, dest, routes)
            if node == dest:
                routes.add(Route([i for i in route], current_time))
                return
            for adj_node in get_station_by_index(node).get_neighbours(current_time.date()):
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
