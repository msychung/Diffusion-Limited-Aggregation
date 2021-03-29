import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
plt.style.use('seaborn-whitegrid')

class Constant_Step():
    '''
    Discrete implementation of scalar standard Brownian motion of a single particle, in the time interval [0, T] with N points ((N - 1) subintervals). Plots positions for 1D, 2D and 3D in discrete space, and calculates values for average displacement and rms displacement over many iterations. Each run of the class should yield a different set of results and output plot. This can be prevented by using a seed to maintain reproducibility, i.e. using np.random.seed(0) and changing the parameter.

    Methods
    -------
    __init__
        Constructor method, sets class variables.

    gen_random_walk
        Creates a random walk in 1D, 2D and 3D with constant step size, using random.choice. 

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
            The number of steps taken by any one walker (particle)

        ss : float
            The (fixed) step size taken by a walker

        iterations : int
            The number of times the simulation is run 
        '''

        self.N = N      # number of steps
        self.ss = ss      # step size
        self.iterations = iterations     # number of iterations

        # Initialise lists containing x, y, z positions and distances. These are lists of zeros of length N
        self.x = [0] * self.N
        self.y = [0] * self.N
        self.z = [0] * self.N
        self.distances = [0] * self.N


    def gen_random_walk(self, dimension): 
        '''
        Creates a random walk with constant step size in 1D, 2D or 3D, using random.choice. 

        Parameters
        ----------
        dimension : str
            Selects which array is returned based on number of random variables
        '''
        
        if dimension == '1D':
            for i in range(1, self.N):
                step = random.choice([-self.ss, self.ss])
                self.x[i] = self.x[i-1] + step
                self.distances[i] = math.sqrt(self.x[i]**2)

            coord_1D = self.x[-1]
        
            ### Only run this if doing a single iteration, otherwise you get lots of print statemente!
            # print('Destination co-ordinates =', coord_1D, ', Distance =', self.distances[-1])

            return coord_1D


        elif dimension == '2D':
            for i in range(1, self.N):
                (dx, dy) = random.choice([(0, self.ss), (0, -self.ss), (self.ss, 0), (-self.ss, 0)])
                self.x[i] = self.x[i-1] + dx
                self.y[i] = self.y[i-1] + dy
                self.distances[i] = math.sqrt(self.x[i]**2 + self.y[i]**2)

            coord_2D = (self.x[-1], self.y[-1])

            ### Only run this if doing a single iteration!
            # print('Destination co-ordinates =', coord_2D, ', Distance =', self.distances[-1])

            return coord_2D


        else:   # dimension == '3D'
            for i in range(1, self.N):
                (dx, dy, dz) = random.choice([(self.ss, 0, 0), (-self.ss, 0, 0), (0, self.ss, 0), (0, -self.ss, 0), (0, 0, self.ss), (0, 0, -self.ss)])
                self.x[i] = self.x[i-1] + dx
                self.y[i] = self.y[i-1] + dy
                self.z[i] = self.z[i-1] + dz
                self.distances[i] = math.sqrt(self.x[i]**2 + self.y[i]**2 + self.z[i]**2)

            coord_3D = (self.x[-1], self.y[-1], self.z[-1])
            
            ### Only run this if doing a single iteration!
            # print('Destination co-ordinates =', coord_3D, ', Distance =', self.distances[-1])

            return coord_3D


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
                coord_1D = self.gen_random_walk('1D')
                all_coord += coord_1D
                all_coord_sq += coord_1D**2

            av_disp = all_coord/self.iterations
            rms_disp = math.sqrt(all_coord_sq/self.iterations)

            print(f"For {self.iterations} iterations and {self.N} steps, the average displacement is {av_disp} and the root-mean-squared displacement is {rms_disp}. The value of (root of N)*(step size) is {self.ss*math.sqrt(self.N)}.")

            return av_disp, rms_disp


        elif dimension == '2D':
            for i in range(self.iterations):
                coord_2D = self.gen_random_walk('2D')
                x, y = coord_2D[0], coord_2D[1]

                all_xcoord += x
                all_ycoord += y

                all_coord_sq += (x + y)**2

            av_disp = (all_xcoord + all_ycoord)/self.iterations
            rms_disp = math.sqrt(all_coord_sq/self.iterations)

            print(f"For {self.iterations} iterations and {self.N} steps, the average displacement is {av_disp} and the root-mean-squared displacement is {rms_disp}. The value of (root of N)*(step size) is {self.ss*math.sqrt(self.N)}.")

            return av_disp, rms_disp


        else:   # dimension == '3D'
            for i in range(self.iterations):
                coord_3D = self.gen_random_walk('3D')
                x, y, z = coord_3D[0], coord_3D[1], coord_3D[2]

                all_xcoord += x
                all_ycoord += y
                all_zcoord += z

                all_coord_sq += (x + y + z)**2

            av_disp = (all_xcoord + all_ycoord + all_zcoord)/self.iterations
            rms_disp = math.sqrt(all_coord_sq/self.iterations)

            print(f"For {self.iterations} iterations and {self.N} steps, the average displacement is {av_disp} and the root-mean-squared displacement is {rms_disp}. The value of (root of N)*(step size) is {self.ss*math.sqrt(self.N)}.")

            return av_disp, rms_disp


    def plot_random_walk(self, dimension):
        '''
        Plots random walks for fixed step size in 1D, 2D and 3D.

        Parameters
        ----------
        dimension : str
            Selects which array is returned based on number of random variables
        '''
        steps = list(range(self.N))
        matplotlib.rcParams.update({'font.size': 9})

        if dimension == '1D':
            ### Unpack return arguments and create time list
            coord_1D = self.gen_random_walk('1D')

            fig, ax = plt.subplots(2, 1)
            fig.set_size_inches(9, 6)
            ### Plot no. of steps against x
            ax[0].plot(steps, self.x, marker='o', markersize=0.4, linewidth=0)
            ax[0].set(xlabel='Number of steps', ylabel='Random Variable $X(t)$', title='1D Brownian Motion Path for Constant Step Size')

            ### Plot no. of steps against distance
            ax[1].plot(steps, self.distances, marker='o', markersize=0.4, linewidth=0)
            ax[1].set(xlabel='Number of steps', ylabel='Distance', title='1D Distance with Number of Steps')
            plt.tight_layout()
            plt.show()  
            

        elif dimension == '2D':
            ### Unpack return arguments
            coord_2D = self.gen_random_walk('2D')

            fig, ax = plt.subplots(2, 1)
            fig.set_size_inches(9, 6)
            ### Plot x against y
            ax[0].plot(self.x, self.y, marker='o', markersize=0.4, linewidth=0)
            ax[0].set(xlabel='Random Variable $X(t)$', ylabel='Random Variable $Y(t)$', title='2D Brownian Motion Path for Constant Step Size')

            ### Plot no. of steps against distance
            ax[1].plot(steps, self.distances, marker='o', markersize=0.4, linewidth=0)
            ax[1].set(xlabel='Number of steps', ylabel='Distance', title='2D Distance with Number of Steps')
            plt.tight_layout()
            plt.show() 


        else:   # dimension = '3D'
            ### Unpack return arguments
            coord_3D = self.gen_random_walk('3D')

            ### Plot x against y and z
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, projection='3d')
            ax.plot(self.x, self.y, self.z, marker='o', markersize=0.4, linewidth=0)
            ax.set(xlabel='Random Variable $X(t)$', ylabel='Random Variable $Y(t)$', zlabel='Random Variable $Z(t)$', title='3D Brownian Motion Path for Constant Step Size')
            plt.show()  

            ### Plot no. of steps against distance
            fig, ax = plt.figure(), plt.axes()
            fig.set_size_inches(9, 3)
            ax.plot(steps, self.distances, marker='o', markersize=0.2, linewidth=0)
            ax.set(xlabel='Number of steps', ylabel='Distance', title='3D Distance with Number of Steps')
            plt.tight_layout()
            plt.show() 


if __name__ == '__main__':
    ### Call method with dimension parameter
    test = Constant_Step(5000, 1, 100000)
    # test.gen_random_walk('3D')
    # test.calc_displacements('3D')
    test.plot_random_walk('3D')
