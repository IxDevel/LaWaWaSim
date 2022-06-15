import pandas as pd

from units.unit import Unit


class UnitsToCsv:
    def __init__(self, units: list[Unit], units_filename: str = 'units.csv'):
        self.__units = units
        self.__units_filename = units_filename

    def dump_to_file(self):
        columns = ['uid', 'plate_number', 'unit_type']
        rows = [[unit.uid, unit.plate_number, unit.unit_type] for unit in self.__units]
        user_data_frame = pd.DataFrame(rows, columns=columns)
        user_data_frame.to_csv('data/'+self.__units_filename, index=False)
