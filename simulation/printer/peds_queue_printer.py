from routes.ped_queue import PedQueue

CreateTripsCSV = 'CSV/' + 'CreateTripsCSV.csv'
prueba = open('CSV/' + 'CreateTripsCSV.csv', 'w')
titulador = 'UserId,TripId,TA,ST,AT,OPED,TPED\n'
prueba.write(titulador)

class PedsQueuePrinter:

    def __init__(self, peds_queue: list[PedQueue]):
        self.__peds_queue = peds_queue

    def log(self):
        for queue in self.__peds_queue:
            print('PedId: {:3d} Users: {}'.format(queue.ped.uid, [user.uid for user in queue.users]))
