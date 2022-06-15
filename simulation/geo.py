import decimal
import math

from routes.peds import Ped
from routes.point import Point
from routes.route import Route


def distance(starting_point: Point, ending_point: Point) -> decimal:
    rad = math.pi / 180
    lat1 = starting_point.latitude
    lat2 = ending_point.latitude
    lon1 = starting_point.longitude
    lon2 = ending_point.longitude
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    r = 6372.795477598
    a = (math.sin(rad * dlat / 2)) ** 2 + math.cos(rad * lat1) * math.cos(rad * lat2) * (
        math.sin(rad * dlon / 2)) ** 2
    dist = 2 * r * math.asin(math.sqrt(a))
    return dist


def estimate_time(unit, ending_point: Point) -> decimal:
    traffic_factor = 0.5
    dist = distance(unit.current_position, ending_point)
    return dist / (unit.average_velocity * traffic_factor)


def linear_displacement(starting_point: Point, ending_point: Point, estimated_time: decimal,
                        time_delta: decimal) -> Point:
    lat1 = starting_point.latitude
    lat2 = ending_point.latitude
    lon1 = starting_point.longitude
    lon2 = ending_point.longitude
    k_lat = (lat2 - lat1) / estimated_time
    k_lon = (lon2 - lon1) / estimated_time
    lat3 = lat1 + k_lat * time_delta
    lon3 = lon1 + k_lon * time_delta
    return Point(lat3, lon3)


# Para calcular la distancia entre un trip
def calculate_distance_between_peds(route: Route, origin_ped: Ped, target_ped: Ped):
    peds = route.peds
    origen_ped_index = 0
    target_ped_index = 0
    total_distance = 0.0
    for i in range(0, len(peds)):
        if peds[i].uid == origin_ped.uid:
            origen_ped_index = i
        elif peds[i].uid == target_ped.uid:
            target_ped_index = i
    ped_index = origen_ped_index
    while ped_index != target_ped_index:
        next_index = ped_index + 1 if ped_index + 1 < len(peds) else 0
        total_distance += distance(peds[ped_index], peds[next_index])
        ped_index = next_index
    return total_distance


# Trata de no usarla
# Para calcular el tiempo de viajes, pero es mejor que uses el delta entre viajes tiempo_inicio | tiempo_fin
def estimate_time_from_distance(route: Route, origin_ped: Ped, target_ped: Ped, unit_velocity: float):
    return calculate_distance_between_peds(route, origin_ped, target_ped) / unit_velocity