import imageio
import math
import numpy as np
from dla_prototype import Application

class Fractal_Dimension():

    def __init__(self):
        cluster = Application(100)
        cluster.on_execute()
        self.position_list = cluster.crystal_position
        self.x0, self.y0 = cluster.start_x, cluster.start_y

    def cluster_mass(self):
        mass = len(self.position_list)
        logMass = np.log(mass)
        return mass, logMass
        

    def cluster_radius(self):
        pos = self.position_list
        x = max(pos[0]) - self.x0
        y = max(pos[1]) - self.y0
        radius = math.sqrt(x**2 + y**2)
        logRadius = np.log(radius)
        return radius, logRadius
        

def print_results(test):
    mass, logMass = test.cluster_mass()
    radius, logRadius = test.cluster_radius()
    print("N = ", mass)
    print("ln(mass) = ", logMass)
    print("ln(radius) = ", logRadius)
    print("radius = ", radius)


if __name__ == '__main__':
    test = Fractal_Dimension()
    print_results(test)