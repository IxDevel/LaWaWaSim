import decimal
import random
from datetime import datetime, timedelta

from input.routes_loader import RoutesLoader
from input.units_loader import UnitsLoader
from input.users_loader import UsersLoader
from passengers.user import User
from routes.ped_queue import PedQueue
from routes.point import Point
from routes.trip import Trip
from simulation.configuration.simulation_config import SimulationConfig
from simulation.geo import estimate_time, distance, linear_displacement, calculate_distance_between_peds
from simulation.printer.peds_queue_printer import PedsQueuePrinter
from simulation.printer.travel_printer import TravelPrinter
from routes.travel import Travel
from simulation.printer.trip_printer import TripPrinter
from units.enums.unit_state_type import UnitStateType
from units.unit import Unit


FinishTripsCSV = 'CSV/' + 'FinishTripsCSV.csv'
prueba = open('CSV/' + 'FinishTripsCSV.csv', 'w')
titulador ='Trip ended,UserId,UnitId,OPED,TPED,TA,ST,AT,DistRec\n'

prueba.write(titulador)


def from_datetime(c_datetime: datetime):
    return datetime(
        year=c_datetime.year,
        month=c_datetime.month,
        day=c_datetime.day,
        hour=c_datetime.hour,
        minute=c_datetime.minute,
        second=c_datetime.second,
        microsecond=c_datetime.microsecond
    )


class WaWaSimulation:

    def __init__(self, config: SimulationConfig = None):
        self.__config = config  # Stores the config for the simulation
        self.__routes_loader = RoutesLoader()
        self.__units_loader = UnitsLoader()
        self.__users_loader = UsersLoader()

        # Stores the routes that are going to be use on the simulation
        self.__routes = self.__routes_loader.load_routes()
        # Stores the units that are going to participate on the simulation
        self.__units = self.__units_loader.load_units()
        # Stores the users that are going to participate on the simulation
        self.__users = self.__users_loader.load_users()

        # List of travels (Unit tracking)
        self.__travels: list[Travel] = []
        # List of Peds queue
        self.__peds_queue: list[PedQueue] = []

        # Trip id
        self.__trip_id = 1
        # Current simulation time
        self.__sim_datetime = config.starting_time
        # Current simulation ending time
        self.__end_sim_datetime = config.ending_time
        # Console travel printer
        self.__travel_printer = TravelPrinter(self.__travels)
        # Console trip printer
        self.__trip_printer = TripPrinter(self.__users)
        # Console ped queue printer
        self.__peds_queue_printer = PedsQueuePrinter(self.__peds_queue)
        # Extra time that is given to finish
        self.__global_delta: decimal = decimal.Decimal('0')
        # List of units in maintenance
        self.__units_at_maintenance: list[Unit] = []

    def simulate(self):
        # Create the unit travels
        self.create_travels()  # Camionetas
        # Create the users trips
        self.create_trips()  # Usuarios
        # Establish the extra time to accomplish the remaining trips
        delta_to_finish_trips = timedelta(minutes=15)
        # Start the simulation
        for current_day in range(0, self.__config.number_of_repeats):
            # Establish simulation time
            self.__sim_datetime = from_datetime(self.__config.starting_time)
            # Establish end of simulation time
            self.__sim_datetime += timedelta(days=current_day)
            # Update de ending time if necessary
            if self.__sim_datetime > self.__end_sim_datetime:
                self.__end_sim_datetime += timedelta(days=1)

            # If not the first day, create new trips (at the first day they are generated in create_trips())
            if current_day > 0:
                self.add_trips()
            # Print the simulation day
            print('Start of day: {:3d} | ST: {:26s} | ET: {:26}'
                  .format(current_day + 1, str(self.__sim_datetime), str(self.__end_sim_datetime)))

            # Run maintenance routine to replace active units (if there are units left)
            self.do_maintenance()

            # La WaWa simulation
            while self.__sim_datetime < self.__end_sim_datetime + delta_to_finish_trips:
                # First unload passenger, the load the new ones
                self.load_unload_passengers()
                # Update distances and time
                self.update_distances_and_time()
                # Add randomly new passengers
                if self.__sim_datetime < self.__end_sim_datetime:
                    self.add_trips()

                # Just for debug purposes
                print('End of simulation round')
                self.__travel_printer.log()
                self.__trip_printer.log()
                self.__peds_queue_printer.log()

            # Restart variables for a new day
            # Remove uncompleted trips
            # Empty the units
            # Set unit to PEDs
            self.prepare_for_new_day()
            # Print the end of the simulation
            print('End of day: {:3d} | ST: {:26s} | ET: {:26}'
                  .format(current_day + 1, str(self.__sim_datetime), str(self.__end_sim_datetime)))

    def add_trips(self):
        """ Add new trips to the simulation using available users """
        # Get available users
        available_users = [u for u in self.__users if u.trip is None]
        # If there is no available users return
        if len(available_users) == 0:
            return
        # For each ped queue append some randoms users
        for ped_queue in self.__peds_queue:
            if len(ped_queue.users) < 3 and random.random() > 0.5 and len(available_users) > 0:
                # Get the current ped associated with that ped
                ped = ped_queue.ped
                #  Get the route related to that ped
                route = [r for r in self.__routes if ped.uid in [p.uid for p in r.peds]][0]
                # Get from the route the others peds
                other_peds = route.get_other_peds(ped)
                # Add random quantity of trips
                for i in range(0, random.randrange(1, 3)):
                    if len(available_users) > 0:
                        # Sort randomly destination peds
                        other_peds.sort(key=lambda x: random.random())
                        # Select the first ped of the list
                        target_ped = other_peds[0]
                        # Get an available user
                        user = available_users.pop(0)
                        # Create a trip for that user on the same route
                        user.trip = Trip(self.__trip_id, self.__sim_datetime, ped, target_ped
                                         , calculate_distance_between_peds(route, ped, target_ped))
                        # Add the user to the ped queue
                        ped_queue.add_user(user)
                        # Increment the trip id counter
                        self.__trip_id += 1
                        # TODO: Esto tienes que colocarlo en un archivo de nombre created_trips_csv va con el que dice,
                        #  create_trips

    def create_travels(self):
        """ Allows to create the travels that record the unit activity for the simulation """
        # Set user index
        unit_index = 0
        # For each route assign units to their peds
        for route in self.__routes:
            # Get the peds from the route
            peds = route.peds
            # Sort randomly the peds
            peds.sort(key=lambda x: random.random())
            # Assign a unit for some peds
            for i in range(0, self.__config.units_per_route):
                # If there are not units_left cancel end the process
                if unit_index >= len(self.__units):
                    break
                # Get current ped
                current_ped = peds[i]
                # Get an  available unit
                unit = self.__units[unit_index]
                # Set unit a the ped
                unit.current_position = Point(current_ped.latitude, current_ped.longitude)
                # Set unit status from inactive to active
                unit.unit_state_type = UnitStateType.active
                # Get next ped
                next_ped = route.get_next(current_ped)
                # Record the travel
                self.__travels.append(Travel(unit, current_ped, next_ped, route, distance(current_ped, next_ped),
                                             estimate_time(unit, next_ped)))
                # Update available unit index
                unit_index += 1
        # For debug purposes
        self.__travel_printer.log()

    def create_trips(self):
        """ Generate user trips previous the simulation """
        # Set user index
        user_index = 0
        # Get available users
        users = self.__users
        # Sort randomly users
        users.sort(key=lambda x: random.random())
        # For each route ped assign a trip
        for route in self.__routes:
            # Get peds from route
            peds = route.peds
            # For each ped create a ped_queue and assign users
            for origin_ped in peds:
                # Get the other peds related with ped
                other_peds = route.get_other_peds(origin_ped)
                # If there is not available users abort
                if user_index >= len(self.__users):
                    break
                # Prepare te users list for the ped_queue
                users: list[User] = []
                # Create the ped queue
                self.__peds_queue.append(PedQueue(origin_ped, users))
                # Add the users to the queue
                for i in range(0, random.randrange(1, 3)):
                    # Set the application time
                    application_time = from_datetime(self.__sim_datetime) # Si no usas esto,se modifica con el tiempo
                    # Choose a ped to arrive
                    arrival_ped = other_peds[random.randrange(0, len(other_peds))]
                    # Get an user
                    user = self.__users[user_index]
                    # Create a trip for the user
                    user.trip = Trip(self.__trip_id, application_time, origin_ped, arrival_ped,
                                     calculate_distance_between_peds(route, origin_ped, arrival_ped))
                    # Append the user to the queue
                    users.append(user)
                    # Update user index and id
                    user_index += 1
                    self.__trip_id += 1
                    # TODO: Esto tienes que colocarlo en un archivo de nombre created_trips_csv donde registras la info,
                    #   de los viajes

        # Debug
        print('Creating initial trips!')
        self.__trip_printer.log()
        self.__peds_queue_printer.log()

    def load_unload_passengers(self):
        """ Load unload passengers from the units"""
        # Get units at ped
        units_at_ped: list[Travel] = []
        for travel in self.__travels:
            # Get the associated unit
            unit = travel.unit
            # if the unit is at ped, then append to the list
            if unit.current_position.latitude == travel.origin_ped.latitude and \
                    unit.current_position.longitude == travel.origin_ped.longitude:
                units_at_ped.append(travel)
                # For debug purposes
                if unit.unit_state_type != UnitStateType.active:
                    print("Invalid unit estate")
                    exit(23)

        # Unload passengers
        for travel in units_at_ped:
            for passenger in travel.unit.passengers:
                # For debug purposes
                if passenger.trip is None:
                    print('Error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    print(passenger.uid)
                    exit(15)
                # If the arrival ped is the unit current ped, then unload the passenger
                if passenger.trip.arrival_ped.uid == travel.origin_ped.uid:
                    # Set passenger arrival time
                    passenger.trip.arrival_time = from_datetime(self.__sim_datetime)
                    # Remove the passenger from the unit
                    travel.unit.remove_passenger(passenger)
                    # TODO: Esto tienes que colocarlo en un archivo de nombre trips_csv registars los elementos para la
                    #   tabla de hechos
                    print('Trip ended: {:3d} | UserId: {:3d} | UnitId: {:3d} | OPED: {:3d} | TPED: {:3d} | '
                          'TA: {:19s} | ST: {:19s} | AT: {:19s} | DistRec: {:12.8f}'
                          .format(passenger.trip.uid, passenger.uid, travel.unit.uid, passenger.trip.starting_ped.uid,
                                  passenger.trip.arrival_ped.uid, str(passenger.trip.time_of_application),
                                  str(passenger.trip.starting_time), str(passenger.trip.arrival_time),
                                  passenger.trip.distance))
                    lista = str('{:3d}'.format(passenger.trip.uid))+','+ str('{:3d}'.format(passenger.uid))+','+str('{:3d}'.format(travel.unit.uid))+','+str('{:3d}'.format(passenger.trip.starting_ped.uid))+','+str('{:3d}'.format(passenger.trip.arrival_ped.uid))+','+str('{:19s}'.format(str(passenger.trip.time_of_application)))+','+str('{:19s}'.format(str(passenger.trip.starting_time)))+','+str('{:19s}'.format(str(passenger.trip.arrival_time)))+','+str('{:12.8f}'.format(passenger.trip.distance))+'\n'
                    prueba.write(lista)
                    # Clear passenger trip
                    passenger.trip = None

        # Load passengers
        for travel in units_at_ped:
            # Get the queue associated with the unit current ped
            current_ped_queue = [q for q in self.__peds_queue if q.ped.uid == travel.origin_ped.uid][0]
            # Get the users from ped_queue
            users = current_ped_queue.users
            # Get the unit from travel
            unit = travel.unit
            # For each user at the ped queue
            for user in users:
                # If the unit is full, abort
                if len(unit.passengers) == unit.seats:
                    break
                # Add the passenger to unit
                unit.add_passenger(user)
                # Remove the curren passenger from the ped queue
                current_ped_queue.remove_user(user)
                # Set starting trip time
                user.trip.starting_time = from_datetime(self.__sim_datetime)

    def update_distances_and_time(self):
        # Get minimum time for an event
        travels = self.__travels.copy()
        # Sort by elapsed_time the available travels
        travels.sort(key=lambda x: x.time_to_arrival)
        # Get de time to arrival
        delta = travels[0].time_to_arrival
        # Convert to a delta time object
        time_delta = timedelta(hours=delta)
        print('Arrival of UnitId: {} | Time delta: {} Current time: {} | New time: {}'
              .format(travels[0].unit.uid, delta * 60, self.__sim_datetime, self.__sim_datetime + time_delta))

        # Update simulation time
        self.__sim_datetime += time_delta

        # Update positions for each unit
        for travel in travels:
            old_current_position = travel.unit.current_position
            # Calculate the new unit position
            travel.unit.current_position = \
                linear_displacement(travel.unit.current_position, travel.target_ped, travel.time_to_arrival, delta)
            # Get the new distance
            travel.distance = distance(travel.unit.current_position, travel.target_ped)
            # Calculate the time to arrival
            travel.time_to_arrival = estimate_time(travel.unit, travel.target_ped)
            # If the time is less than 10 seconds, put the unit at the ped
            if travel.time_to_arrival * 3600 < 10:
                # Get update the origin ped to the last target ped
                travel.origin_ped = travel.target_ped
                # Get the next target ped
                travel.target_ped = travel.route.get_next(travel.origin_ped)
                # Calculate the distance
                travel.distance = distance(travel.origin_ped, travel.target_ped)
                # Calculate the time to arrive to the target ped
                travel.time_to_arrival = estimate_time(travel.unit, travel.target_ped)
                # Assign the position
                travel.unit.current_position = Point(travel.origin_ped.latitude, travel.origin_ped.longitude)
            # TODO: Hazle debug a esto porfa
            new_current_position = travel.unit.current_position
            print(travel.unit.mileage)
            print(distance(old_current_position, new_current_position))
            travel.unit.mileage = travel.unit.mileage + distance(old_current_position, new_current_position)
            # Todo: Aqui es donde guardas la informacion de los transportes: id, routeId
            #  , cantidad de pasajeros, ubicacion de la unidad, parada de inicio, parada de final, kilometraje
            #  el nombre del archivo travels.csv

    def prepare_for_new_day(self):
        # Set fixed position to units
        for travel in self.__travels:
            # Remove all passengers remaining from the units
            travel.unit.remove_all_passengers()
            # Update the unit position to the travel ped
            travel.unit.current_position = Point(travel.origin_ped.latitude, travel.origin_ped.longitude)
            # Reset distance of the unit (move to ped)
            travel.distance = distance(travel.origin_ped, travel.target_ped)
            # Reset the time to arrival of the unit
            travel.time_to_arrival = estimate_time(travel.unit, travel.target_ped)

        # Empty ped queues
        for ped_queue in self.__peds_queue:
            ped_queue.remove_all_users()

        # Clean user trips
        for user in self.__users:
            user.trip = None

    def do_maintenance(self):
        # Finish maintenance of old units
        for unit in self.__units_at_maintenance:
            if random.random() > 5:
                # Set unit status to inactive
                unit.unit_state_type = UnitStateType.inactive
                print('UnitId {:3d} left maintenance at {:26s}'.format(unit.uid, str(self.__sim_datetime)))
                # TODO: Aqui haces el log de las unidades que salen del mantenimiento maintenance_out.csv
        # Update the maintenance unit list
        self.__units_at_maintenance = [unit for unit in self.__units_at_maintenance if unit.unit_state_type.repairing]

        # Add new units to repairing
        replacement_units = [unit for unit in self.__units if unit.unit_state_type == UnitStateType.inactive]
        for travel in self.__travels:
            if random.random() > 0.9:
                if len(replacement_units) == 0:
                    break
                # Select unit to maintain
                unit_to_maintenance = travel.unit
                # Update unit status from active to repairing
                unit_to_maintenance.unit_state_type = UnitStateType.repairing
                # Get replacement unit
                replacement_unit = replacement_units.pop(0)
                # Update replacement unit status from inactive to active
                replacement_unit.unit_state_type = UnitStateType.active
                # Deploy the replacement unit on the same position where the other unit was
                replacement_unit.current_position = unit_to_maintenance.current_position
                # Unset to unit position
                unit_to_maintenance.current_position = None
                # Replace the unit
                travel.unit = replacement_unit
                # TODO: Aqui haces el log de las unidades que entran al mantenimiento maintenance_in.csv
