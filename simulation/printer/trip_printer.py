from passengers.user import User


class TripPrinter:

    def __init__(self, users: list[User]):
        self.__users = users

    def log(self):
        for user in [u for u in self.__users if u.trip is not None]:
            print('UserId: {:3d} | TripId: {:3d} | TA: {:26s} | ST: {:26s} | AT: {:26s} | OPED: {:3d} | TPED: {:3d}'.
                  format(user.uid, user.trip.uid, str(user.trip.time_of_application),
                         '--' if user.trip.starting_time is None else str(user.trip.starting_time),
                         '--' if user.trip.arrival_time is None else str(user.trip.arrival_time),
                         user.trip.starting_ped.uid, user.trip.arrival_ped.uid))
