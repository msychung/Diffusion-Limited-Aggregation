import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import random
from random import random
plt.style.use('seaborn-whitegrid')


class BrownianMotion():
    '''
    Implementation of scalar standard Brownian motion, in the time interval [0, T] with N points ((N - 1) subintervals).
    '''
    def __init__(self):
        pass


    def line(self):
        '''
        Produces a scatter plot of x co-ordinates against y co-ordinates, following a y = x line with minor deviations. 
        Should produce a slightly different plot each time (because it's random..!), better approximating a straight line y = x for a greater N. 
        '''
        # Initialise parameters
        T = 10.0    # time step
        N = 100     # number of steps
        h = math.sqrt(T/N)

        '''For larger N, it is more efficient to append to lists then call the dataframe constructor, than to create an empty dataframe and append to it.
        This is because pandas append() returns a copy of the original df and the new one (quadratic copy with complexity O(N^2))'''
        x_list = []
        y_list = []

        for i in range(1, N + 1):
            '''random() generates a random number from the uniform distribution'''
            x = i + h * random()
            y = i + h * random()

            x_list.append(x)
            y_list.append(y)

        df = pd.DataFrame({'x': x_list, 'y': y_list})
        del x_list, y_list

        fig, ax = plt.figure(), plt.axes()
        ax.plot(df['x'], df['y'], marker='o', markersize=1, linewidth=0)
        ax.set(xlabel='x', ylabel='y', title='x-y plot')
        plt.show()


    def brownian_motion_1D(self):
        '''
        1D Brownian Motion Path
        '''
        # Initialise parameters
        T = 1.0    # time step
        N = 10000     # number of steps
        dt = math.sqrt(T/(N-1))    # sqrt of time interval

        '''For larger N, it is more efficient to append to lists then call the dataframe constructor, than to create an empty dataframe and append to it.
        This is because pandas append() returns a copy of the original df and the new one (quadratic copy with complexity O(N^2))'''

        t = np.linspace(0, T, N)
        x = [0] * N    # Random variable x
        dx = [0] * N     # Increment dx

        dx[0] = dt * np.random.randn()
        x[0] = dx[0]

        for i in range (1, N):
            '''np.random.randn() generates a random number from the standard normal distribution'''
            dx[i] = dt * np.random.normal()
            x[i] = x[i-1] + dx[i] 

        df = pd.DataFrame({'t': t, 'x': x, 'dx': dx})
        del t, x, dx

        fig, ax = plt.figure(), plt.axes()
        ax.plot(df['t'], df['x'], marker='o', markersize=1, linewidth=0)
        ax.set(xlabel='Time t', ylabel='Random Variable $X(t)$', title='1D Brownian Motion Path')
        plt.show()  


    def brownian_motion_2D(self):
        '''
        2D Brownian Motion Path
        '''
        # Initialise parameters
        T = 1.0    # time step
        N = 10000     # number of steps
        dt = math.sqrt(T/(N-1))    # sqrt of time interval

        '''For larger N, it is more efficient to append to lists then call the dataframe constructor, than to create an empty dataframe and append to it.
        This is because pandas append() returns a copy of the original df and the new one (quadratic copy with complexity O(N^2))'''

        t = np.linspace(0, T, N)

        x = [0] * N    # Random variable x
        dx = [0] * N     # Increment dx

        dx[0] = dt * np.random.randn()
        x[0] = dx[0]

        y = [0] * N    # Random variable y
        dy = [0] * N    # Increment dx

        dy[0] = dt * np.random.randn()
        y[0] = dy[0]

        for i in range (1, N):
            '''np.random.randn() generates a random number from the standard normal distribution'''
            dx[i] = dt * np.random.normal()
            x[i] = x[i-1] + dx[i] 

            dy[i] = dt * np.random.normal()
            y[i] = y[i-1] + dy[i] 

        df = pd.DataFrame({'t': t, 'x': x, 'dx': dx, 'y': y, 'dy': dy})
        del t, x, dx, y, dy

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(df['t'], df['x'], df['y'], marker='o', markersize=1, linewidth=0)
        ax.set_xlabel('Time t')
        ax.set_ylabel('Random Variable $X(t)$')
        ax.set_zlabel('Random Variable $Y(t)$')
        ax.title.set_text('2D Brownian Motion')
        plt.show()  

test = BrownianMotion()
test.brownian_motion_2D()
