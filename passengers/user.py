import json

from routes.trip import Trip


class User:
    def __init__(self, uid: int, trip: Trip = None):
        self.__uid: int = uid
        self.__trip = trip

    def __repr__(self):
        return "User()"

    def __str__(self):
        return json.dumps(self.__dict__)

    @property
    def uid(self):
        return self.__uid

    @property
    def trip(self):
        return self.__trip

    @trip.setter
    def trip(self, trip: Trip):
        self.__trip = trip
