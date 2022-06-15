import decimal

from routes.peds import Ped
from routes.route import Route
from units.unit import Unit


class Travel:

    def __init__(self, unit: Unit,
                 origin_ped: Ped,
                 target_ped: Ped,
                 route: Route,
                 distance: decimal,
                 time_to_arrival: decimal):
        self.__unit = unit
        self.__origin_ped = origin_ped
        self.__target_ped = target_ped
        self.__route = route
        self.__distance = distance
        self.__time_to_arrival: decimal = time_to_arrival

    def __repr__(self):
        return 'Travel()'

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, unit: Unit):
        self.__unit = unit

    @property
    def origin_ped(self):
        return self.__origin_ped

    @origin_ped.setter
    def origin_ped(self, ped: Ped):
        self.__origin_ped = ped

    @property
    def target_ped(self):
        return self.__target_ped

    @target_ped.setter
    def target_ped(self, ped: Ped):
        self.__target_ped = ped

    @property
    def route(self):
        return self.__route

    @property
    def distance(self):
        return self.__distance

    @distance.setter
    def distance(self, distance: decimal):
        self.__distance = distance

    @property
    def time_to_arrival(self) -> decimal:
        return self.__time_to_arrival

    @time_to_arrival.setter
    def time_to_arrival(self, time_to_arrival: decimal):
        self.__time_to_arrival = time_to_arrival
