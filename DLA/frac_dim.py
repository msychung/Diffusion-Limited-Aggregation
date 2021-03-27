import imageio
import math
import numpy as np
from dla_prototype import Application

class Fractal_Dimension():

    def __init__(self):
        cluster = Application(200, 'dot', 'square', 'square', 50, 100, 20)
        cluster.on_execute()
        self.position_list = cluster.crystal_position
        self.x0, self.y0 = cluster.start_x, cluster.start_y

    def cluster_mass(self):
        mass = len(self.position_list)
        logMass = np.log(mass)
        return mass, logMass
        
    
    def cluster_radius(self):
        max_radius = 0
        for cluster in self.position_list:
            x = cluster[0] - self.x0
            y = cluster[1] - self.y0
            radius = np.sqrt(x**2 + y**2)
        
            if radius > max_radius:
                max_radius = radius

        logRadius = np.log(math.floor(max_radius))
        return math.floor(max_radius), logRadius


def print_results(test):
    mass, logMass = test.cluster_mass()
    radius, logRadius = test.cluster_radius()
    print("N = ", mass)
    print("ln(mass) = ", logMass)
    print("radius = ", radius)
    print("ln(radius) = ", logRadius)


if __name__ == '__main__':
    test = Fractal_Dimension()
    print_results(test)