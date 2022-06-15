import pandas as pd

from passengers.user import User


class UsersToCsv:
    def __init__(self, users: list[User], users_filename: str = 'users.csv'):
        self.__users = users
        self.__users_filename = users_filename

    def dump_to_file(self):
        columns = ['uid']
        rows = [[user.uid] for user in self.__users]
        user_data_frame = pd.DataFrame(rows, columns=columns)
        user_data_frame.to_csv('data/'+self.__users_filename, index=False)
