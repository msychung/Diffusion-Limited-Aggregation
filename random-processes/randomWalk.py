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

        x_list = []
        y_list = []

        for i in range(1, N + 1):
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

test = BrownianMotion()
test.line()