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
    Implementation of scalar standard Brownian motion, in the time interval [0, T] with N points ((N - 1) subintervals). Begins with a simple y = x plot, before plotting positions for 1D, 2D and 3D Brownian motion. Each time, a different set of results and output plot should be produced. This can be prevented by using a seed to maintain reproducibility, using np.random.seed(0) and changing the parameter.

    Methods
    -------
    __init__
        Constructor method, sets class variables and random seed

    xy_line
        Plotting a rough x-y line using random module

    brownian_1D_loop
        1D Brownian motion for a single path, using a for loop

    brownian_1D_vec
        1D Brownian motion for multiple maths, using a vectorised method

    brownian_2D_loop
        2D Brownian motion for a single path, using a for loop

    brownian_2D_vec
        2D Brownian motion for multiple maths, using a vectorised method

    brownian_3D_vec
        3D Brownian motion for multiple maths, using a vectorised method
    '''

    def __init__(self, T, N, M):
        np.random.seed(5)
        
        self.T = T    # time step
        self.N = N    # number of steps
        self.M = M    # number of paths ('walkers')
        
        self.dt = math.sqrt(T/(N-1))    # sqrt of time interval
        self.t = np.linspace(0, T, N)    # Create time list (from 0 to T with step size T/N)


    def xy_line(self):
        '''
        Practising use of pseudo-RNGs, dataframes and plotting.
        Produces a scatter plot of x co-ordinates against y co-ordinates, following a y = x line with minor deviations. 
        Should produce a slightly different plot each time (because it's random..!), better approximating a straight line y = x for a greater N. 
        '''
        ### Initialise method parameters
        h = math.sqrt(self.T/self.N)

        '''For larger N, it is more efficient to append to lists then call the dataframe constructor, than to create an empty dataframe and append to it.
        This is because pandas append() returns a copy of the original df and the new one (quadratic copy with complexity O(N^2))'''
        
        ### Create empty lists
        x_list = []
        y_list = []

        ### Loop to fill lists 
        for i in range(1, self.N + 1):
            '''random() generates a random number from the uniform distribution'''
            x = i + h * random()
            y = i + h * random()

            x_list.append(x)
            y_list.append(y)

        ### Create dataframe and fill with lists, then delete lists
        df = pd.DataFrame({'x': x_list, 'y': y_list})
        del x_list, y_list

        ### Plot x against y 
        fig, ax = plt.figure(), plt.axes()
        ax.plot(df['x'], df['y'], marker='o', markersize=1, linewidth=0)
        ax.set(xlabel='x', ylabel='y', title='x-y plot')
        plt.show()


    def brownian_1D_loop(self):
        '''
        1D Brownian Motion Path for a single walker, using a for loop
        '''
        ### Create lists of zeroes of length N
        x = [0] * self.N    # Random variable x
        dx = [0] * self.N     # Increment dx

        ### Set initial values 
        dx[0] = self.dt * np.random.randn()  # multiples time interval by some random number in the SNN
        x[0] = dx[0]

        ### Loop to fill rest of the elements of the lists
        for i in range (1, self.N):
            '''np.random.randn() generates a random number from the standard normal distribution'''
            dx[i] = self.dt * np.random.normal()
            x[i] = x[i-1] + dx[i] 

        ### Create dataframe and fill with lists, then delete lists
        df = pd.DataFrame({'t': self.t, 'x': x, 'dx': dx})
        del x, dx

        ### Plot t against x 
        fig, ax = plt.figure(), plt.axes()
        ax.plot(df['t'], df['x'], marker='o', markersize=1, linewidth=0)
        ax.set(xlabel='Time t', ylabel='Random Variable $X(t)$', title='1D Brownian Motion Single Path')
        plt.show()  


    def brownian_1D_vec(self):
        '''
        1D Brownian Motion Path, using vectorised method and for multiple (M) walkers
        '''
        ### Vectorised method for multiple paths (MxN array)
        dx = self.dt * np.random.randn(self.M, self.N)
        x = np.cumsum(dx, axis = 1)
        
        ### Assign values into a dataframe
        df = pd.DataFrame(x).T      # takes transpose to flip rows/columns
        df.insert(0, 'Time', self.t, True)

        ### Plot t against x 
        fig, ax = plt.figure(), plt.axes()

        # Aesthetics: cycles through a colormap
        ax.set_prop_cycle('color', plt.cm.winter(np.linspace(0, 4, self.M*4)))  

        for i in range(self.M):
            ax.plot(df['Time'], df.iloc[:, i+1], marker='o', markersize=0.25, linewidth=0)

        ax.set(xlabel='Time t', ylabel='Random Variable $X(t)$', title='1D Brownian Motion Multiple Paths (Variable Step Size)')

        plt.show()  


    def brownian_2D_loop(self):
        '''
        2D Brownian Motion Path for a single walker, using a for loop
        '''
        ### Create lists of zeroes of length N
        x = [0] * self.N    # Random variable x
        dx = [0] * self.N     # Increment dx

        y = [0] * self.N    # Random variable y
        dy = [0] * self.N    # Increment dx

        ### Set initial values 
        dx[0] = self.dt * np.random.randn()
        x[0] = dx[0]

        dy[0] = self.dt * np.random.randn()
        y[0] = dy[0]

        ### Loop to fill rest of the elements of the lists
        for i in range (1, self.N):
            '''np.random.randn() generates a random number from the standard normal distribution'''
            dx[i] = self.dt * np.random.normal()
            x[i] = x[i-1] + dx[i] 

            dy[i] = self.dt * np.random.normal()
            y[i] = y[i-1] + dy[i] 

        ### Create dataframe and fill with lists, then delete lists
        df = pd.DataFrame({'t': self.t, 'x': x, 'dx': dx, 'y': y, 'dy': dy})
        del x, dx, y, dy

        ### Plot x against y
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # for i in range(M):
        ax.plot(df['x'], df['y'], marker='o', markersize=1, linewidth=0.5)
        
        ax.set_xlabel('Random Variable $X(t)$')
        ax.set_ylabel('Random Variable $Y(t)$')
        ax.title.set_text('2D Brownian Motion Single Path (Variable Step Size)')

        plt.show()  


    def brownian_2D_vec(self):
        '''
        2D Brownian Motion Path, using vectorised method and for multiple (M) walkers
        '''
        ### Vectorised method for multiple paths (MxN array)
        dx = self.dt * np.random.randn(self.M, self.N)
        x = np.cumsum(dx, axis = 1)

        dy = self.dt * np.random.randn(self.M, self.N)
        y = np.cumsum(dy, axis = 1)
        
        ### Assign values into a dataframe
        df_x = pd.DataFrame(x).T
        df_y = pd.DataFrame(y).T
        df_join = pd.concat([df_x, df_y], axis = 1)
        df_join.insert(0, 'Time', self.t, True)

        ### Plot x against y 
        fig, ax = plt.figure(), plt.axes()

        # Aesthetics: cycles through a colormap
        ax.set_prop_cycle('color', plt.cm.winter(np.linspace(0, 4, self.M*4)))  

        for i in range(self.M):
            ax.plot(df_join.iloc[:, i+1], df_join.iloc[:, i+1+self.M], marker='o', markersize=0.25, linewidth=0.2)

        ax.set(xlabel='Random Variable $X(t)$', ylabel='Random Variable $Y(t)$', title='2D Brownian Motion Multiple Paths (Variable Step Size)')

        plt.show()  


    def brownian_3D_vec(self):
        '''
        3D Brownian Motion Path, using vectorised method and for multiple (M) walkers
        '''
        ### Vectorised method for multiple paths (MxN array)
        dx = self.dt * np.random.randn(self.M, self.N)
        x = np.cumsum(dx, axis = 1)

        dy = self.dt * np.random.randn(self.M, self.N)
        y = np.cumsum(dy, axis = 1)

        dz = self.dt * np.random.randn(self.M, self.N)
        z = np.cumsum(dz, axis = 1)
        
        ### Assign values into a dataframe
        df_x = pd.DataFrame(x).T
        df_y = pd.DataFrame(y).T
        df_z = pd.DataFrame(z).T
        df_join = pd.concat([df_x, df_y, df_z], axis = 1)
        df_join.insert(0, 'Time', self.t, True)

        ### Plot x against y and z
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')

        # Aesthetics: cycles through a colormap
        ax.set_prop_cycle('color', plt.cm.winter(np.linspace(0, 4, self.M*4)))  

        for i in range(self.M):
            ax.plot(df_join.iloc[:, i+1], df_join.iloc[:, i+1+self.M], df_join.iloc[:, i+1+self.M+self.M], marker='o', markersize=0.25, linewidth=0.2)

        ax.set(xlabel='Random Variable $X(t)$', ylabel='Random Variable $Y(t)$', zlabel='Random Variable $Z(t)$', title='3D Brownian Motion Multiple Paths (Variable Step Size)')

        plt.show()  


if __name__ == '__main__':
    ### Create instance of class and call relevant method
    test = BrownianMotion(1.0, 1000, 5)
    test.brownian_2D_loop()
