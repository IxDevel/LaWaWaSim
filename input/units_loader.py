import pandas as pd

from units.bus import Bus
from units.unit import Unit
from units.van import Van


class UnitsLoader:
    def __init__(self, units_filename: str = 'units.csv'):
        self.__units_filename = units_filename

    def load_units(self):
        units_data = pd.read_csv('data/' + self.__units_filename)
        units: list[Unit] = []
        for i in units_data.index:
            if units_data.unit_type[i] == 'Bus':
                unit = Bus(units_data.uid[i], units_data.plate_number[i])
            else:
                unit = Van(units_data.uid[i], units_data.plate_number[i])
            units.append(unit)
        return units
