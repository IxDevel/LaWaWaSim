from routes.point import Point
from simulation.configuration.simulation_config import SimulationConfig
from simulation.geo import distance
from simulation.wawa_simulation import WaWaSimulation

if __name__ == '__main__':
    #a1 = Point(10.50333226, -66.91572819)
    #a2 = Point(10.5001187, -66.91182427)
    #a3 = Point(10.49939995, -66.90270525)
    #a4 = Point(10.49714788, -66.88535095)
    #a5 = Point(10.50154502, -66.89852628)
    #res = distance(a5,a1) + distance(a1, a2) + distance(a2, a3) + distance(a3, a4)
    #print("Distancia de la 115 a la 114 es de : " + str(res))

    config = SimulationConfig()
    simulation = WaWaSimulation(config)
    simulation.simulate()

