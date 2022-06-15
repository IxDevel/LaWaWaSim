import pandas as pd

from passengers.user import User


class UsersLoader:
    def __init__(self, users_filename: str = 'users.csv'):
        self.__users_filename = users_filename

    def load_users(self):
        users_data = pd.read_csv('data/' + self.__users_filename)
        users = list[User]()
        for i in users_data.index:
            user = User(users_data.uid[i])
            users.append(user)
        return users
