from passengers.user import User
from units.enums.unit_type import UnitType
from units.unit import Unit


class Van(Unit):

    def __init__(self,
                 uid: int,
                 plate_number: str):
        super().__init__(uid, plate_number, 6, 45, UnitType.van)

    def __repr__(self):
        return "Van()"
