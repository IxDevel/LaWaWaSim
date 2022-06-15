from passengers.user import User


class UsersGenerator:

    def __init__(self, max_users: int = 1000):
        self.__max_users: int = max_users
        self.__users: list[User] = []

        for _ in range(1, self.__max_users + 1):
            self.__users.append(User(_))

        for _ in self.__users:
            print(_)

    @property
    def max_users(self):
        return self.__max_users

    @property
    def users(self):
        return self.__users
