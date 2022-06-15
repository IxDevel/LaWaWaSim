import pandas as pd

from routes.peds import Ped
from routes.route import Route


class RoutesLoader:
    def __init__(self, routes_filename: str = 'routes.csv', peds_filename: str = 'peds.csv'):
        self.__routes_filename = routes_filename
        self.__peds_filename = peds_filename

    def load_routes(self):
        peds_data = pd.read_csv('data/' + self.__peds_filename)
        peds_by_route_id = dict[int, list[Ped]]()
        for i in peds_data.index:
            ped = Ped(peds_data.owner_id[i],
                      peds_data.route_id[i],
                      peds_data.uid[i],
                      peds_data.name[i],
                      peds_data.latitude[i],
                      peds_data.longitude[i])
            peds: list[Ped] = peds_by_route_id.get(peds_data.route_id[i], list[Ped]())
            peds.append(ped)
            if len(peds) == 1:
                peds_by_route_id[peds_data.route_id[i]] = peds

        routes_data = pd.read_csv('data/' + self.__routes_filename)
        routes = list[Route]()
        for i in routes_data.index:
            route = Route(routes_data.owner_id[i],
                          routes_data.uid[i],
                          routes_data.name[i],
                          peds_by_route_id[routes_data.uid[i]])
            routes.append(route)

        for i in range(0, 3):
            print(routes[i])

        return routes
