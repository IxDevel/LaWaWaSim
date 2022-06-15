from datetime import datetime

import pandas as pd


class SimulationConfig:
    def __init__(self,
                 config_filename: str = 'config.csv'):
        self.__config_filename = config_filename
        config_data = pd.read_csv('data/' + self.__config_filename)

        self.__starting_time = datetime(
            year=config_data.year[0],
            month=config_data.month[0],
            day=config_data.day[0],
            hour=config_data.starting_hour[0],
            minute=0,
            second=0,
            microsecond=0
        )
        self.__ending_time = datetime(
            year=config_data.year[0],
            month=config_data.month[0],
            day=config_data.day[0],
            hour=config_data.ending_hour[0],
            minute=0,
            second=0,
            microsecond=0
        )
        self.__units_per_route = int(config_data.units_per_route[0])
        self.__owner_id = int(config_data.owner_id[0])
        self.__number_of_repeats = int(config_data.number_repeats[0])
        print('Configuracion cargada: ST: {:19s} | ET: {:19s} | UPR: {:3d} | OID: {:3d} | NRP: {:3d}'
              .format(str(self.__starting_time), str(self.__ending_time), self.__units_per_route, self.__owner_id,
                      self.__number_of_repeats))

    @property
    def starting_time(self) -> datetime:
        return self.__starting_time

    @property
    def ending_time(self) -> datetime:
        return self.__ending_time

    @property
    def units_per_route(self):
        return self.__units_per_route

    @property
    def owner_id(self):
        return self.__owner_id

    @property
    def number_of_repeats(self):
        return self.__number_of_repeats
