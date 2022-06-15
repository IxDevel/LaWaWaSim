from routes.travel import Travel


class TravelPrinter:

    def __init__(self, travels: list[Travel]):
        self.__travels = travels

    def log(self):
        for travel in self.__travels:
            print('UnitId: {:3d} | Lat: {:10.8f} | Lon: {:10.8f} | DistR: {:12.8f} | '
                  'OPedId: {:3d} | TPedId: {:3d} | Dis: {:10.8f} Km | ETA: {:10.8f} min | '
                  'RouteOwner: {:3d} | RouteId: {:3d}'
                  .format(travel.unit.uid, travel.unit.current_position.latitude,
                          travel.unit.current_position.longitude, travel.unit.mileage,
                          travel.origin_ped.uid, travel.target_ped.uid,
                          travel.distance, travel.time_to_arrival * 60,  travel.route.owner_id, travel.route.uid))
