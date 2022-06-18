from routes.travel import Travel

TravelsCSV = 'CSV/' + 'TravelsCSV.csv'
prueba = open('CSV/' + 'TravelsCSV.csv', 'w')
titulador = 'UnitId,Lat,Lon,DistR,OPedId,TPedId,Dis,ETA,RouteOwner,RouteId,Pasajeros\n'
prueba.write(titulador)


class TravelPrinter:

    def __init__(self, travels: list[Travel]):
        self.__travels = travels



    def log(self):

        """

        :rtype: object
        """
        for travel in self.__travels:
            print(' UnitId: {:3d} | Lat: {:10.8f} | Lon: {:10.8f} | DistR: {:12.8f} | '
                  'OPedId: {:3d} | TPedId: {:3d} | Dis: {:10.8f} Km | ETA: {:10.8f} min | '
                  'RouteOwner: {:3d} | RouteId: {:3d}'
                  .format(travel.unit.uid, travel.unit.current_position.latitude,
                          travel.unit.current_position.longitude, travel.unit.mileage,
                          travel.origin_ped.uid, travel.target_ped.uid,
                          travel.distance, travel.time_to_arrival * 60,  travel.route.owner_id, travel.route.uid))
            lista = str('{:3d}'.format(travel.unit.uid)) + ',' + str('{:10.8f}'.format(travel.unit.current_position.latitude)) + ',' + str('{:10.8f}'.format(travel.unit.current_position.longitude)) + ',' + str('{:12.8f}'.format(travel.unit.mileage)) + ',' + str('{:3d}'.format(travel.origin_ped.uid)) + ',' + str('{:3d}'.format(travel.target_ped.uid)) + ',' + str('{:10.8f}'.format(travel.distance)) + ',' + str('{:10.8f}'.format(travel.time_to_arrival * 60)) + ',' + str('{:3d}'.format(travel.route.owner_id)) + ',' + str('{:3d}'.format(travel.route.uid))+ ',' + str('{:3d}'.format(len(travel.unit.passengers)))+'\n'
            prueba.write(lista)