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

class Constant_Step():
    '''
    Implementation of scalar standard Brownian motion, in the time interval [0, T] with N points ((N - 1) subintervals). Begins with a simple y = x plot, before plotting positions for 1D, 2D and 3D Brownian motion. Each time, a different set of results and output plot should be produced. This can be prevented by using a seed to maintain reproducibility, using np.random.seed(0) and changing the parameter.

    Methods
    -------
    __init__
        Constructor method, sets class variables.

    gen_random_walk
        Creates a random walk with constant step size, using np.random.choice. 

    calc_displacements
        Calculates and prints average displacement and rms displacement over many iterations, for random walks in 1D, 2D and 3D.

    plot_random_walk
        Plots random walks for fixed step size in 1D, 2D and 3D.
    '''

    def __init__(self, N, ss, iterations):
        '''
        Initialise the parameters every time an instance of the class is called. 

        Parameters
        ----------
        N : int
            The number of steps taken by any one walker

        ss : float
            The (fixed) step size

        iterations : int
            The number of times the simulation is run 
        '''
        self.N = N      # number of steps
        self.ss = ss      # step size
        self.iterations = iterations     # number of iterations

        self.x = [0] * self.N
        self.y = [0] * self.N
        self.z = [0] * self.N
        self.distances = [0] * self.N


    def gen_random_walk(self, dimension): 
        '''
        Creates a random walk with constant step size, using np.random.choice. 

        Parameters
        ----------
        dimension : str
            Selects which array is returned based on number of random variables
        '''

        ### Create lists of zeros of length N and set first value to 0
        
        ss = self.ss
        x = self.x
        y = self.y
        z = self.z
        distances = self.distances
        
        if dimension == '1D':
            for i in range(1, self.N):
                step = random.choice([-ss, ss])

                x[i] = x[i-1] + step
                distances[i] = math.sqrt(x[i]**2)

            coord_1D = x[-1]

            ### Only run this if doing a single iteration!
            # print('Destination co-ordinates =', coord_1D, ', Distance =', distances[-1])

            return x, coord_1D, distances[-1]


        elif dimension == '2D':
            for i in range(1, self.N):
                (dx, dy) = random.choice([(0, ss), (0, -ss), (ss, 0), (-ss, 0)])

                x[i] = x[i-1] + dx
                y[i] = y[i-1] + dy
                distances[i] = math.sqrt(x[i]**2 + y[i]**2)

            coord_2D = (x[-1], y[-1])

            ### Only run this if doing a single iteration!
            # print('Destination co-ordinates =', coord_2D, ', Distance =', distances[-1])

            return x, y, coord_2D, distances


        else:   # dimension == '3D'
            for i in range(1, self.N):
                (dx, dy, dz) = random.choice([(ss, 0, 0), (-ss, 0, 0), (0, ss, 0), (0, -ss, 0), (0, 0, ss), (0, 0, -ss)])

                x[i] = x[i-1] + dx
                y[i] = y[i-1] + dy
                z[i] = z[i-1] + dz
                distances[i] = math.sqrt(x[i]**2 + y[i]**2 + z[i]**2)

            coord_3D = (x[-1], y[-1], z[-1])
            
            ### Only run this if doing a single iteration!
            # print('Destination co-ordinates =', coord_3D, ', Distance =', distances[-1])

            return x, y, z, coord_3D, distances


    def calc_displacements(self, dimension):
        '''
        Calculates average displacement and rms displacement over many iterations, for random walks in 1D, 2D and 3D.

        Parameters
        ----------
        dimension : str
            Selects which array is returned based on number of random variables
        '''
        
        all_coord, all_xcoord, all_ycoord, all_zcoord, all_coord_sq = 0, 0, 0, 0, 0

        if dimension == '1D':
            for i in range(self.iterations):
                coord_1D = self.gen_random_walk('1D')[1]

                all_coord += coord_1D
                all_coord_sq += coord_1D**2

            av_disp = all_coord/self.iterations
            rms_disp = math.sqrt(all_coord_sq/self.iterations)

            print(f"For {self.iterations} iterations and {self.N} steps, the average displacement is {av_disp} and the root-mean-squared displacement is {rms_disp}. The value of (root of N)*(step size) is {self.ss*math.sqrt(self.N)}.")


        elif dimension == '2D':
            for i in range(self.iterations):
                coord_2D = self.gen_random_walk('2D')[2]
                x, y = coord_2D[0], coord_2D[1]

                all_xcoord += x
                all_ycoord += y

                all_coord_sq += (x + y)**2

            av_disp = (all_xcoord + all_ycoord)/self.iterations
            rms_disp = math.sqrt(all_coord_sq/self.iterations)

            print(f"For {self.iterations} iterations and {self.N} steps, the average displacement is {av_disp} and the root-mean-squared displacement is {rms_disp}. The value of (root of N)*(step size) is {self.ss*math.sqrt(self.N)}.")


        else:   # dimension == '3D'
            for i in range(self.iterations):
                coord_3D = self.gen_random_walk('3D')[3]
                x, y, z = coord_3D[0], coord_3D[1], coord_3D[2]

                all_xcoord += x
                all_ycoord += y
                all_zcoord += z

                all_coord_sq += (x + y + z)**2

            av_disp = (all_xcoord + all_ycoord + all_zcoord)/self.iterations
            rms_disp = math.sqrt(all_coord_sq/self.iterations)

            print(f"For {self.iterations} iterations and {self.N} steps, the average displacement is {av_disp} and the root-mean-squared displacement is {rms_disp}. The value of (root of N)*(step size) is {self.ss*math.sqrt(self.N)}.")


    def plot_random_walk(self, dimension):
        '''
        Plots random walks for fixed step size in 1D, 2D and 3D.

        Parameters
        ----------
        dimension : str
            Selects which array is returned based on number of random variables
        '''

        steps = list(range(self.N))

        if dimension == '1D':
            ### Unpack return arguments and create time list
            x, coord_1D, distances = self.gen_random_walk('1D')

            fig, ax = plt.subplots(2, 1)
            fig.set_size_inches(8, 6)
            ### Plot no. of steps against x
            ax[0].plot(steps, x, marker='o', markersize=0.5, linewidth=0)
            ax[0].set(xlabel='Number of steps', ylabel='Random Variable $X(t)$', title='1D Brownian Motion Path for Fixed Step Size')

            ### Plot no. of steps against distance
            ax[1].plot(steps, self.distances, marker='o', markersize=0.5, linewidth=0)
            ax[1].set(xlabel='Number of steps', ylabel='Distance', title='1D Distance with Number of Steps')
            plt.tight_layout()
            plt.show()  
            

        elif dimension == '2D':
            ### Unpack return arguments
            x, y, coord_2D, distances = self.gen_random_walk('2D')

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
            x, y, z, coord_3D, distances = self.gen_random_walk('3D')

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


if __name__ == '__main__':
    ### Call method with dimension parameter
    test = Constant_Step(2000, 1, 10000)
    # test.gen_random_walk('3D')
    test.calc_displacements('3D')
    # test.plot_random_walk('3D')