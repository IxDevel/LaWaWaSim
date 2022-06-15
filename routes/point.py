import decimal
import json


class Point:

    def __init__(self,
                 latitude: decimal,
                 longitude: decimal):
        self.__latitude: decimal = latitude
        self.__longitude: decimal = longitude

    def __repr__(self):
        return "Point()"

    def __str__(self):
        return json.dumps(self.__dict__)

    @property
    def latitude(self):
        return self.__latitude

    @property
    def longitude(self):
        return self.__longitude
