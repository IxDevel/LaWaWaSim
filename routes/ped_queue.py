from passengers.user import User
from routes.peds import Ped


class PedQueue:

    def __init__(self, ped: Ped, users: list[User]):
        self.__ped = ped
        self.__users = users

    @property
    def ped(self):
        return self.__ped

    @property
    def users(self):
        return self.__users.copy()

    @users.setter
    def users(self, users: list[User]):
        self.__users = users

    def remove_user(self, target_user: User):
        self.__users = [user for user in self.__users if user.uid != target_user.uid]

    def remove_all_users(self):
        self.__users.clear()

    def add_user(self, user: User):
        self.__users.append(user)
