import decimal

from routes.point import Point


class Ped(Point):

    def __init__(self,
                 owner_id: int,
                 route_id: int,
                 uid: int,
                 name: str,
                 latitude: decimal,
                 longitude: decimal):
        self.__owner_id = owner_id
        self.__route_id = route_id
        self.__uid = uid
        self.__name = name
        super().__init__(latitude, longitude)

    def __repr__(self):
        return "Ped()"

    @property
    def uid(self):
        return self.__uid

    @property
    def name(self):
        return self.__name


