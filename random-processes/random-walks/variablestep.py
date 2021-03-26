import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler
from numpy import random
from random import random
plt.style.use('seaborn-whitegrid')


class Variable_Step():
    '''
    Implementation of scalar standard Brownian motion, in the time interval [0, T] with N points ((N - 1) subintervals). Plots positions for 1D, 2D and 3D Brownian motion. Each time, a different set of results and output plot should be produced. This can be prevented by using a seed to maintain reproducibility, using np.random.seed(0) and changing the parameter.

    Methods
    -------
    __init__
        Constructor method, sets class variables and random seed

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

    def __init__(self, T, N, M, iterations):
        '''
        Initialise the parameters every time an instance of the class is called. 

        Parameters
        ----------
        T : float
            The total time for which the simulation is run

        N : int
            The number of steps taken by any one walker

        M : int
            The number of walkers

        iterations : int
            The number of iterations of one simulation
        '''
        np.random.seed(5)

        self.T = T    # total simulation time
        self.N = N    # number of steps
        self.M = M    # number of paths ('walkers')
        self.iterations = iterations    # number of iterations of one simulation
        
        self.dt = math.sqrt(T/(N-1))    # sqrt of time interval
        self.t = np.linspace(0, T, N)    # create time list (from 0 to T with step size T/N)


    def brownian_1D_loop(self, plot=True):
        '''
        1D Brownian Motion Path for a single walker, using a for loop
        Plot parameter set to False when method called in calc_displacements() for displacement calculations
        '''
        ### Create lists of zeroes of length N
        x = [0] * self.N    # Random variable x
        dx = [0] * self.N     # Increment dx

        ### Set initial values 
        dx[0] = x[0] = self.dt * np.random.randn()  # multiplies time interval by some random number in the SNN

        ### Loop to fill rest of the elements of the lists
        for i in range (1, self.N):
            '''np.random.randn() generates a random number from the standard normal distribution'''
            dx[i] = self.dt * np.random.normal()
            x[i] = x[i-1] + dx[i] 
       
        ## Create dataframe and fill with lists, then delete lists
        df = pd.DataFrame({'t': self.t, 'x': x, 'dx': dx})
        del x, dx

        if plot == True:
            ### Plot t against x 
            fig, ax = plt.figure(), plt.axes()
            ax.plot(df['t'], df['x'], marker='o', markersize=1, linewidth=0)
            ax.set(xlabel='Time t', ylabel='Random Variable $X(t)$', title='1D Brownian Motion Single Path')
            plt.show()  

        return df


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
        
        return df


    def brownian_2D_loop(self, plot=True):
        '''
        2D Brownian Motion Path for a single walker, using a for loop
        '''
        ### Create lists of zeroes of length N
        x = [0] * self.N    # Random variable x
        dx = [0] * self.N     # Increment dx

        y = [0] * self.N    # Random variable y
        dy = [0] * self.N    # Increment dy

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

        if plot == True:
            ### Plot x against y
            fig = plt.figure()
            ax = fig.add_subplot(111)

            # for i in range(M):
            ax.plot(df['x'], df['y'], marker='o', markersize=1, linewidth=0.5)
            
            ax.set_xlabel('Random Variable $X(t)$')
            ax.set_ylabel('Random Variable $Y(t)$')
            ax.title.set_text('2D Brownian Motion Single Path (Variable Step Size)')

            plt.show()  

        return df


    def brownian_2D_vec(self):
        '''
        2D Brownian Motion Path, using vectorised method and for multiple (M) walkers
        Plot parameter set to False when method called in calc_displacements() for displacement calculations
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

        return df_join


    def brownian_3D_loop(self, plot=True):
        '''
        3D Brownian Motion Path for a single walker, using a for loop
        '''
        ### Create lists of zeroes of length N
        x = [0] * self.N    # Random variable x
        dx = [0] * self.N     # Increment dx

        y = [0] * self.N    # Random variable y
        dy = [0] * self.N    # Increment dy

        z = [0] * self.N    # Random variable z
        dz = [0] * self.N    # Increment dz

        ### Set initial values 
        dx[0] = self.dt * np.random.randn()
        x[0] = dx[0]

        dy[0] = self.dt * np.random.randn()
        y[0] = dy[0]

        dz[0] = self.dt * np.random.randn()
        z[0] = dz[0]

        ### Loop to fill rest of the elements of the lists
        for i in range (1, self.N):
            '''np.random.randn() generates a random number from the standard normal distribution'''
            dx[i] = self.dt * np.random.normal()
            x[i] = x[i-1] + dx[i] 

            dy[i] = self.dt * np.random.normal()
            y[i] = y[i-1] + dy[i] 

            dz[i] = self.dt * np.random.normal()
            z[i] = z[i-1] + dz[i] 

        ### Create dataframe and fill with lists, then delete lists
        df = pd.DataFrame({'t': self.t, 'x': x, 'dx': dx, 'y': y, 'dy': dy, 'z': z, 'dz': dz})
        del x, dx, y, dy, z, dz

        if plot == True:
            ### Plot x against y and z
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, projection='3d')
            ax.plot(df['x'], df['y'], df['z'], marker='o', markersize=1, linewidth=0.5)
            ax.set(xlabel='Random Variable $X(t)$', ylabel='Random Variable $Y(t)$', zlabel='Random Variable $Z(t)$', title='3D Brownian Motion Path Single Path (Variable Step Size)')
            plt.show()  

        return df


    def brownian_3D_vec(self):
        '''
        3D Brownian Motion Path, using vectorised method and for multiple (M) walkers
        Plot parameter set to False when method called in calc_displacements() for displacement calculations
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

        return df_join


    def calc_displacements(self, dimension):
        '''
        Calculates average displacement over many iterations, for random walks in 1D, 2D and 3D.
        N.B. The rms displacement has no clear relation to N for variable step size. 

        Parameters
        ----------
        dimension : str
            Selects which array is returned based on number of random variables
        '''

        all_coord, all_xcoord, all_ycoord, all_zcoord, all_coord_sq = 0, 0, 0, 0, 0

        if dimension == '1D':
            for i in range(self.iterations):
                df = self.brownian_1D_loop(plot=False)
                coord_1D = df['x'].iloc[-1]
                # mean_length = abs(df['dx'].mean())

                all_coord += coord_1D
                # all_coord_sq += coord_1D**2      

            av_disp = all_coord/self.iterations
            # rms_disp = math.sqrt(all_coord_sq/self.iterations)

            print(f"For {self.iterations} iterations and {self.N} steps, the average displacement is {av_disp}.")
            
            return av_disp

        elif dimension == '2D':
            for i in range(self.iterations):
                df = self.brownian_2D_loop(plot=False)
                x = df['x'].iloc[-1]
                y = df['y'].iloc[-1]

                all_xcoord += x
                all_ycoord += y

            av_disp = (all_xcoord + all_ycoord)/self.iterations

            print(f"For {self.iterations} iterations and {self.N} steps, the average displacement is {av_disp}.")

            return av_disp

        else:   # dimension == '3D'
            for i in range(self.iterations):
                df = self.brownian_3D_loop(plot=False)
                x = df['x'].iloc[-1]
                y = df['y'].iloc[-1]
                z = df['z'].iloc[-1]

                all_xcoord += x
                all_ycoord += y
                all_zcoord += z

            av_disp = (all_xcoord + all_ycoord + all_zcoord)/self.iterations

            print(f"For {self.iterations} iterations and {self.N} steps, the average displacement is {av_disp}.")

            return av_disp


if __name__ == '__main__':
    ### Create instance of class and call relevant method
    test = Variable_Step(1.0, 1000, 5, 100)
    # test.brownian_3D_loop()
    # test.calc_displacements('3D')