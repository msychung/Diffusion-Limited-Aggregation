import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from cycler import cycler
import random
# from numpy import random
# from random import random
plt.style.use('seaborn-whitegrid')


def random_walk(dimension): 
    '''
    Creates a random walk with constant step size, using np.random.choice. 

    Parameters
    ----------
    dimension : str
        Selects which array is returned based on number of random variables
    '''

    ### Initialise parameters
    N = 100      # number of steps
    x = 0    # one dimension
    y = 0    # two dimensions
    z = 0    # three dimensions

    if dimension == '1D':
        for i in range(N + 1):
            step = random.choice([-1, 1])
            x += step

        print('Destination co-ordinates =', x, 'Distance =', math.sqrt(x**2))

    elif dimension == '2D':
        for i in range(N + 1):
            (dx, dy) = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

            x += dx
            y += dy

        print('Destination co-ordinates =', (x, y), 'Distance =', math.sqrt(x**2 + y **2))

    else:   # dimension == '3D'
        for i in range(N + 1):
            (dx, dy, dz) = random.choice([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)])

            x += dx
            y += dy
            z += dz

        print('Destination co-ordinates =', (x, y, z), 'Distance =', math.sqrt(x**2 + y **2 + z**2))


### Call method with dimension parameter
random_walk('3D')