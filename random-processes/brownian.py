import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler
from numpy import random
from random import random
plt.style.use('seaborn-whitegrid')


class BrownianMotion():
    '''
    Implementation of scalar standard Brownian motion, in the time interval [0, T] with N points ((N - 1) subintervals). Begins with a simple y = x plot, before plotting positions for 1D and 2D Brownian motion. Each time, a different set of results and output plot should be produced.
    '''
    def __init__(self):
        pass
        # Might need to put something in here later on...


    def line(self):
        '''
        Produces a scatter plot of x co-ordinates against y co-ordinates, following a y = x line with minor deviations. 
        Should produce a slightly different plot each time (because it's random..!), better approximating a straight line y = x for a greater N. 
        '''
        # Initialise parameters
        T = 10.0    # time step
        N = 101     # number of steps (+1 to give N-1 subintervals)
        h = math.sqrt(T/N)

        '''For larger N, it is more efficient to append to lists then call the dataframe constructor, than to create an empty dataframe and append to it.
        This is because pandas append() returns a copy of the original df and the new one (quadratic copy with complexity O(N^2))'''
        
        # Create empty lists
        x_list = []
        y_list = []

        # Loop to fill lists 
        for i in range(1, N + 1):
            '''random() generates a random number from the uniform distribution'''
            x = i + h * random()
            y = i + h * random()

            x_list.append(x)
            y_list.append(y)

        # Create dataframe and fill with lists, then delete lists
        df = pd.DataFrame({'x': x_list, 'y': y_list})
        del x_list, y_list

        # Plot x against y 
        fig, ax = plt.figure(), plt.axes()
        ax.plot(df['x'], df['y'], marker='o', markersize=1, linewidth=0)
        ax.set(xlabel='x', ylabel='y', title='x-y plot')
        plt.show()


    def brownian_1D(self):
        '''
        1D Brownian Motion Path, using a for loop
        '''
        # Initialise parameters
        T = 1.0    # time step
        N = 10001     # number of steps (+1 to give N-1 subintervals)
        dt = math.sqrt(T/(N-1))    # sqrt of time interval

        '''For larger N, it is more efficient to append to lists then call the dataframe constructor, than to create an empty dataframe and append to it.
        This is because pandas append() returns a copy of the original df and the new one (quadratic copy with complexity O(N^2))'''

        t = np.linspace(0, T, N)    # Create time list

        # Create lists of zeroes of length N
        x = [0] * N    # Random variable x
        dx = [0] * N     # Increment dx

        # Set initial values 
        dx[0] = dt * np.random.randn()
        x[0] = dx[0]

        # Loop to fill rest of the elements of the lists
        for i in range (1, N):
            '''np.random.randn() generates a random number from the standard normal distribution'''
            dx[i] = dt * np.random.normal()
            x[i] = x[i-1] + dx[i] 

        # Create dataframe and fill with lists, then delete lists
        df = pd.DataFrame({'t': t, 'x': x, 'dx': dx})
        del t, x, dx

        # Plot t against x 
        fig, ax = plt.figure(), plt.axes()
        ax.plot(df['t'], df['x'], marker='o', markersize=1, linewidth=0)
        ax.set(xlabel='Time t', ylabel='Random Variable $X(t)$', title='1D Brownian Motion Path')
        plt.show()  


    def brownian_1D_vec(self):
        '''
        1D Brownian Motion Path, using vectorised method and for multiple (M) paths
        '''
        # Initialise parameters
        T = 1.0    # time step
        N = 1001     # number of steps (+1 to give N-1 subintervals)
        M = 10    # number of paths ('walkers')
        dt = math.sqrt(T/(N-1))    # sqrt of time interval

        '''For larger N, it is more efficient to append to lists then call the dataframe constructor, than to create an empty dataframe and append to it.
        This is because pandas append() returns a copy of the original df and the new one (quadratic copy with complexity O(N^2))'''

        t = np.linspace(0, T, N)    # Create time list

        dx = dt * np.random.randn(M, N)
        x = np.cumsum(dx, axis = 1)

        # Plot t against x 
        fig, ax = plt.figure(), plt.axes()

        # Aesthetics: cycles through a colormap
        ax.set_prop_cycle('color', plt.cm.winter(np.linspace(0, 4, 45)))  

        for i in range(M):
            ax.plot(t, x[i,:], marker='o', markersize=0.25, linewidth=0)

        ax.set(xlabel='Time t', ylabel='Random Variable $X(t)$', title='1D Brownian Motion Multiple Paths')

        plt.show()  


    def brownian_2D(self):
        '''
        2D Brownian Motion Path
        '''
        # Initialise parameters
        T = 1.0    # time step
        N = 1001     # number of steps (+1 to give N-1 subintervals)
        dt = math.sqrt(T/(N-1))    # sqrt of time interval

        '''For larger N, it is more efficient to append to lists then call the dataframe constructor, than to create an empty dataframe and append to it.
        This is because pandas append() returns a copy of the original df and the new one (quadratic copy with complexity O(N^2))'''

        t = np.linspace(0, T, N)    # Create time list

        # Create lists of zeroes of length N
        x = [0] * N    # Random variable x
        dx = [0] * N     # Increment dx

        y = [0] * N    # Random variable y
        dy = [0] * N    # Increment dx

        # Set initial values 
        dx[0] = dt * np.random.randn()
        x[0] = dx[0]

        dy[0] = dt * np.random.randn()
        y[0] = dy[0]

        # Loop to fill rest of the elements of the lists
        for i in range (1, N):
            '''np.random.randn() generates a random number from the standard normal distribution'''
            dx[i] = dt * np.random.normal()
            x[i] = x[i-1] + dx[i] 

            dy[i] = dt * np.random.normal()
            y[i] = y[i-1] + dy[i] 

        # Create dataframe and fill with lists, then delete lists
        df = pd.DataFrame({'t': t, 'x': x, 'dx': dx, 'y': y, 'dy': dy})
        del t, x, dx, y, dy

        # Plot t against x and y
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(df['x'], df['y'], marker='o', markersize=1, linewidth=0.5)
        ax.set_xlabel('Random Variable $X(t)$')
        ax.set_ylabel('Random Variable $Y(t)$')
        ax.title.set_text('2D Brownian Motion')
        plt.show()  


# Create instance of class and call relevant method
test = BrownianMotion()
test.brownian_2D()