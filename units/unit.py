import json

from passengers.user import User
from routes.peds import Ped
from routes.point import Point
from units.enums.unit_state_type import UnitStateType
from units.enums.unit_type import UnitType


class Unit:

    def __init__(self,
                 uid: int,
                 plate_number: str,
                 seats: int,
                 average_velocity: float,
                 unit_type: UnitType,
                 passengers: list[User] = None,
                 current_position: Point = None,
                 unit_state_type: UnitStateType = UnitStateType.inactive):
        self.__uid: int = uid
        self.__plate_number: str = plate_number
        self.__seats: int = seats
        self.__passengers: list[User] = [] if passengers is None else passengers
        self.__average_velocity: float = average_velocity
        self.__unit_type: UnitType = unit_type
        self.__current_position = current_position
        self.__unit_state_type = unit_state_type
        self.__mileage = 0.0

    def __repr__(self):
        return "Unit()"

    def __str__(self):
        return json.dumps(self.__dict__)

    @property
    def uid(self):
        return self.__uid

    @property
    def plate_number(self):
        return self.__plate_number

    @property
    def seats(self):
        return self.__seats

    @property
    def average_velocity(self):
        return self.__average_velocity

    @property
    def unit_type(self):
        return self.__unit_type

    @property
    def passengers(self):
        return self.__passengers.copy()

    @property
    def current_position(self):
        return self.__current_position

    @current_position.setter
    def current_position(self, point: Point):
        self.__current_position = point

    @property
    def unit_state_type(self):
        return self.__unit_state_type

    @unit_state_type.setter
    def unit_state_type(self, state: UnitStateType):
        self.__unit_state_type = state

    def get_passengers_by_ped(self, ped: Ped):
        return [user for user in self.__passengers if user.trip.uid == ped.uid]

    def add_passenger(self, user: User):
        self.__passengers.append(user)

    def remove_passenger(self, user: User):
        self.__passengers = [p for p in self.__passengers if p.uid != user.uid]
        for p in self.__passengers:
            if p.uid == user.uid:
                print('Esta funcionando mal')
                exit(9)

    def remove_all_passengers(self):
        self.__passengers.clear()

    @property
    def mileage(self):
        return self.__mileage

    @mileage.setter
    def mileage(self, mileage: float):
        self.__mileage = mileage
