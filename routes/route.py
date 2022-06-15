import json

from routes.peds import Ped
from routes.point import Point


class Route:

    def __init__(self,
                 owner_id: int,
                 uid: int,
                 name: str,
                 peds: list[Ped]):
        self.__owner_id = owner_id
        self.__uid = uid
        self.__name = name
        self.__peds = peds

    def __repr__(self):
        return "Route()"

    def __str__(self):
        return f'owner: {self.__owner_id}, uid: {self.__uid}, name: {self.name}, peds: {self.__peds}'

    @property
    def owner_id(self):
        return self.__owner_id

    @property
    def uid(self):
        return self.__uid

    @property
    def name(self):
        return self.__name

    @property
    def peds(self):
        return self.__peds.copy()

    def get_other_peds(self, current_ped: Ped):
        return [ped for ped in self.__peds if ped.uid != current_ped.uid]

    def get_next(self, current_point: Ped):
        index = self.__peds.index(current_point)
        if index < len(self.__peds)-1:
            return self.__peds[index+1]
        return self.__peds[0]
