import decimal
import json
from datetime import datetime

from routes.peds import Ped


class Trip:

    def __init__(self,
                 uid: int,
                 time_of_application: datetime,
                 starting_ped: Ped,
                 arrival_ped: Ped,
                 distance: decimal,
                 starting_time: datetime = None,
                 arrival_time: datetime = None):
        self.__uid = uid
        self.__time_of_application = time_of_application
        self.__starting_time = starting_time
        self.__arrival_time = arrival_time
        self.__starting_ped = starting_ped
        self.__arrival_ped = arrival_ped
        self.__distance = distance

    def __repr__(self):
        return "Trip()"

    def __str__(self):
        return json.dumps(self.__dict__)

    @property
    def uid(self):
        return self.__uid

    @property
    def time_of_application(self):
        return self.__time_of_application

    @property
    def starting_time(self):
        return self.__starting_time

    @starting_time.setter
    def starting_time(self, starting_time: datetime):
        self.__starting_time = starting_time

    @property
    def arrival_time(self):
        return self.__arrival_time

    @arrival_time.setter
    def arrival_time(self, arrival_time: datetime):
        self.__arrival_time = arrival_time

    @property
    def starting_ped(self):
        return self.__starting_ped

    @property
    def arrival_ped(self):
        return self.__arrival_ped

    @property
    def distance(self):
        return self.__distance
