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


N = 10000      # number of steps

def calc_random_walk(dimension): 
    '''
    Creates a random walk with constant step size, using np.random.choice. 

    Parameters
    ----------
    dimension : str
        Selects which array is returned based on number of random variables
    '''

    ### Create lists of zeros of length N and set first value to 0
    x = [0] * N
    y = [0] * N
    z = [0] * N
    distances = [0] * N


    if dimension == '1D':
        for i in range(1, N):
            step = random.choice([-1, 1])

            x[i] = x[i-1] + step
            distances[i] = math.sqrt(x[i]**2)

        coord_1D = x[-1]

        print('Destination co-ordinates =', coord_1D, ', Distance =', distances[-1])

        return x, coord_1D, distances


    elif dimension == '2D':
        for i in range(1, N):
            (dx, dy) = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

            x[i] = x[i-1] + dx
            y[i] = y[i-1] + dy
            distances[i] = math.sqrt(x[i]**2 + y[i]**2)

        coord_2D = (x[-1], y[-1])

        print('Destination co-ordinates =', coord_2D, ', Distance =', distances[-1])

        return x, y, coord_2D, distances


    else:   # dimension == '3D'
        for i in range(1, N):
            (dx, dy, dz) = random.choice([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)])

            x[i] = x[i-1] + dx
            y[i] = y[i-1] + dy
            z[i] = z[i-1] + dz
            distances[i] = math.sqrt(x[i]**2 + y[i]**2 + z[i]**2)

        coord_3D = (x[-1], y[-1], z[-1])
        
        print('Destination co-ordinates =', coord_3D, ', Distance =', distances[-1])

        return x, y, z, coord_3D, distances


def plot_random_walk(dimension):
    '''
    Plots random walks for fixed step size in 1D, 2D and 3D.

    Parameters
    ----------
    dimension : str
        Selects which array is returned based on number of random variables
    '''

    steps = list(range(N))

    if dimension == '1D':
        ### Unpack return arguments and create time list
        x, coord_1D, distances = calc_random_walk('1D')

        fig, ax = plt.subplots(2, 1)
        fig.set_size_inches(8, 6)
        ### Plot no. of steps against x
        ax[0].plot(steps, x, marker='o', markersize=0.5, linewidth=0)
        ax[0].set(xlabel='Number of steps', ylabel='Random Variable $X(t)$', title='1D Brownian Motion Path for Fixed Step Size')

        ### Plot no. of steps against distance
        ax[1].plot(steps, distances, marker='o', markersize=0.5, linewidth=0)
        ax[1].set(xlabel='Number of steps', ylabel='Distance', title='1D Distance with Number of Steps')
        plt.tight_layout()
        plt.show()  
        

    elif dimension == '2D':
        ### Unpack return arguments
        x, y, coord_2D, distances = calc_random_walk('2D')

        fig, ax = plt.subplots(2, 1)
        fig.set_size_inches(8, 6)
        ### Plot x against y
        ax[0].plot(x, y, marker='o', markersize=1, linewidth=0.3)
        ax[0].set(xlabel='Random Variable $X(t)$', ylabel='Random Variable $Y(t)$', title='2D Brownian Motion Path for Fixed Step Size')

        ### Plot no. of steps against distance
        ax[1].plot(steps, distances, marker='o', markersize=0.5, linewidth=0)
        ax[1].set(xlabel='Number of steps', ylabel='Distance', title='2D Distance with Number of Steps')
        plt.tight_layout()
        plt.show() 


    else:   # dimension = '3D'
        ### Unpack return arguments
        x, y, z, coord_3D, distances = calc_random_walk('3D')

        ### Plot x against y and z
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot(x, y, z, marker='o', markersize=0.5, linewidth=0)
        ax.set(xlabel='Random Variable $X(t)$', ylabel='Random Variable $Y(t)$', zlabel='Random Variable $Z(t)$', title='3D Brownian Motion Path for Fixed Step Size')
        plt.show()  

        ### Plot no. of steps against distance
        fig, ax = plt.figure(), plt.axes()
        fig.set_size_inches(9, 5)
        ax.plot(steps, distances, marker='o', markersize=0.5, linewidth=0)
        ax.set(xlabel='Number of steps', ylabel='Distance', title='3D Distance with Number of Steps')
        plt.tight_layout()
        plt.show() 



### Call method with dimension parameter
plot_random_walk('3D')