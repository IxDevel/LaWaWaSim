import enum
import json


class UnitType(str, enum.Enum):
    bus = "Bus"
    van = "Van"

    def __repr__(self):
        return "Van()"

    def __str__(self):
        return json.dumps(self.__dict__)
