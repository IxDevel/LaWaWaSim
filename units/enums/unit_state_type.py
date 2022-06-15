import enum
import json


class UnitStateType(str, enum.Enum):
    active = "Active"
    repairing = "Repairing"
    inactive = "Inactive"

    def __repr__(self):
        return "UnitStateType()"

    def __str__(self):
        return json.dumps(self.__dict__)
