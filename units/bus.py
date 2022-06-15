from units.enums.unit_type import UnitType
from units.unit import Unit


class Bus(Unit):

    def __init__(self,
                 uid: int,
                 plate_number: str):
        super().__init__(uid, plate_number, 15, 45, UnitType.bus)

    def __repr__(self):
        return "Bus()"
