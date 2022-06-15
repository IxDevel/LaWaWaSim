import random

from units.bus import Bus
from units.unit import Unit
from units.van import Van


class UnitsGenerator:

    def __init__(self, max_units: int = 10):
        self.__max_units = max_units
        self.__units: list[Unit] = []
        for _ in range(1, self.__max_units + 1):
            if random.randrange(0, 10) < 8:
                self.__units.append(Bus(_, str(hash(_))[::6]))
            else:
                self.__units.append(Van(_, str(hash(_))[::6]))
        for _ in self.units:
            print(_)

    @property
    def max_units(self):
        return self.__max_units

    @property
    def units(self):
        return self.__units
