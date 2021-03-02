import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy import random
from random import random


class BrownianAnimation():
    '''
    Animating the 1D, 2D and 3D Brownian motion of one and many paths.

        Animation objects are created using the FuncAnimation() method.
        Parameters
        ----------
        fig : Figure
            Figure object used to animate upon
        func : callable
            Callable method to call at each frame
        frames : int
            Number of frames, set to N+1 since range taken
        fargs : tuple or None
            Additional arguments to pass to each call of func
        interval : int, default 200
            Delay between frames in ms
        repeat : bool, default True
            Whether the animation repeats after completion
        
    '''
    # # The random state can be set to maintain reproducibility:
    # np.random.seed(0)


    def __init__(self):
        pass


    def generate_random_walks(self, dt, N, dimension):
        '''
        Create a random walk line using scalar Brownian motion equations (as in brownian_prototype.py).
        Note that there is variable step size due to using np.random.randn(1,N), a standard normal distribution.

        Parameters
        ----------
        dt : float
            The square root of the time interval T/(N-1)
        N : int
            The number of steps
        dimension : str
            Selects which array is returned based on number of random variables
        '''
        pos = np.linspace(0, 1000, 1001)    # no. of steps, for 1D plot

        dx = np.sqrt(dt) * np.random.randn(1, N)
        x = np.cumsum(dx, axis=1)

        dy = np.sqrt(dt) * np.random.randn(1, N)
        y = np.cumsum(dy, axis=1)

        dz = np.sqrt(dt) * np.random.randn(1, N)
        z = np.cumsum(dz, axis=1)

        ### Creates nested lists, vertically stacking the random variables into numpy arrays for 2D and 3D 
        linedata_1D = np.vstack((pos, x))
        linedata_2D = np.vstack((x, y))
        linedata_3D = np.vstack((x, y, z))

        ### Returns an array of shape (dimension, N)
        if dimension == '1D':
            return linedata_1D
        elif dimension == '2D':
            return linedata_2D
        else:   # dimension == '3D'
            return linedata_3D


    def update_random_walks(self, num, walkData, lines, dimension):
        ''' 
        Returns the Line2D objects to update each frame of the animaton. The zip() function combines multiple lists in parallel by collecting items at each position into a single tuple. 

        Parameters
        ----------
        num : int
            Number of frames
        walkData : list
            walkData list passed in
        lines : list
            lines list passed in
        dimension : str
            Selects which Line2D object is returned based on number of random variables
        '''

        for line, data in zip(lines, walkData):
            if dimension == '1D':
                line.set_data(data[0:2, 0:num])

            if dimension == '2D':
                line.set_data(data[0:2, 0:num])

            elif dimension == '3D':   # dimension == '3D'
                line.set_data(data[0:2, :num])
                line.set_3d_properties(data[2, 0:num])

        return lines


    def animate(self, dimension):
        '''
        Creates animations in 1D, 2D and 3D, using matplotlib.animation.

        Parameters
        ----------
        dimension : str
            Selects whether the animation is plotted in 1D, 2D or 3D
        '''

        ### Initialise parameters as previously
        T = 1.0   
        N = 1001 
        dt = math.sqrt(T/(N-1))    

        ### Put lineData list into another list (needed for matplotlib.lines.Line2D module)
        walkData = [self.generate_random_walks(dt, N, dimension)]

        if dimension == '1D':
            pos = walkData[0][0]
            x = walkData[0][1]

        elif dimension == '2D':
            x = walkData[0][0]
            y = walkData[0][1]

        else:   # dimension == '3D'
            x = walkData[0][0]
            y = walkData[0][1]
            z = walkData[0][2]

        ### Create figure and axis objects with tight axes
        fig = plt.figure()

        if dimension == '1D':
            ax = fig.add_subplot(1, 1, 1)
            ax = plt.axes(xlim=(min(pos)+0.1*min(pos), max(pos)+0.1*max(pos)), ylim=(min(x)+0.1*min(x), max(x)+0.1*max(x)))
            ax.set_xlabel('Number of steps')
            ax.set_ylabel('X(t)')
            ax.set_title('1D Discretised Brownian Path')

        elif dimension == '2D':
            ax = fig.add_subplot(1, 1, 1)
            ax = plt.axes(xlim=(min(x)+0.1*min(x), max(x)+0.1*max(x)), ylim=(min(y)+0.1*min(y), max(y)+0.1*max(y)))
            ax.set_xlabel('X(t)')
            ax.set_ylabel('Y(t)')
            ax.set_title('2D Discretised Brownian Paths')

        else:   # dimension == '3D'
            ax = fig.add_subplot(1, 1, 1, projection='3d')
            ax.set_xlabel('X(t)')
            ax.set_xlim3d((min(x)+0.1*min(x), max(x)+0.1*max(x)))
            ax.set_ylabel('Y(t)')
            ax.set_ylim3d((min(y)+0.1*min(y), max(y)+0.1*max(y)))
            ax.set_zlabel('Z(t)')
            ax.set_zlim3d((min(z)+0.1*min(z), max(z)+0.1*max(z)))
            ax.set_title('3D Discretised Brownian Paths')

        ### Use list comprehension to create a list of Line2D Objects
        if dimension == '1D' or '2D':
            lines = [ax.plot(data[0, 0:1], data[1, 0:1])[0] for data in walkData]
        
        else:   # dimension == '3D'
            lines = [ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1])[0] for data in walkData]

        ### Create animation object using the FuncAnimation() method
        anim = animation.FuncAnimation(
        fig, self.update_random_walks, N+1, fargs=(walkData, lines, dimension), interval=30, repeat=True, blit=False)

        plt.show()


    def animation_1D(self):
        ### Initialise parameters as previously
        T = 1.0   
        N = 1001 
        dt = math.sqrt(T/(N-1))    

        ### Put lineData list into another list (needed for matplotlib.lines.Line2D module)
        walkData = [self.generate_random_walks(dt, N, '1D')]
        pos = walkData[0][0]
        x = walkData[0][1]

        ### Create figure and axis objects with tight axes
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax = plt.axes(xlim=(min(pos)+0.1*min(pos), max(pos)+0.1*max(pos)), ylim=(min(x)+0.1*min(x), max(x)+0.1*max(x)))
        
        ax.set_xlabel('Number of steps')
        ax.set_ylabel('X(t)')
        ax.set_title('1D Discretised Brownian Path')

        ### Use list comprehension to create a list of Line2D Objects
        lines = [ax.plot(data[0, 0:1], data[1, 0:1])[0] for data in walkData]
        
        ### Create animation object using the FuncAnimation() method
        anim = animation.FuncAnimation(
            fig, self.update_random_walks, N+1, fargs=(walkData, lines, '1D'), interval=30, repeat=True)

        plt.show()


    def animation_2D(self):
        ### Initialise parameters as previously
        T = 1.0   
        N = 1001 
        dt = math.sqrt(T/(N-1))    

        ### Put lineData list into another list (needed for matplotlib.lines.Line2D module)
        walkData = [self.generate_random_walks(dt, N, '2D')]
        x = walkData[0][0]
        y = walkData[0][1]

        ### Create figure and axis objects with tight axes
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax = plt.axes(xlim=(min(x)+0.1*min(x), max(x)+0.1*max(x)), ylim=(min(y)+0.1*min(y), max(y)+0.1*max(y)))

        ax.set_xlabel('X(t)')
        ax.set_ylabel('Y(t)')
        ax.set_title('2D Discretised Brownian Paths')

        ### Use list comprehension to create a list of Line2D Objects
        lines = [ax.plot(data[0, 0:1], data[1, 0:1])[0] for data in walkData]

        ### Create animation object using the FuncAnimation() method
        anim = animation.FuncAnimation(
            fig, self.update_random_walks, N+1, fargs=(walkData, lines, '2D'), interval=30, repeat=True)

        plt.show()


    def animation_3D(self):
        ### Initialise parameters as previously
        T = 1.0   
        N = 1001 
        dt = math.sqrt(T/(N-1))  

        ### Put lineData list into another list (needed for matplotlib.lines.Line2D module)
        walkData = [self.generate_random_walks(dt, N, '3D')]
        x = walkData[0][0]
        y = walkData[0][1]
        z = walkData[0][2]

        ### Create figure and axis objects with tight axes
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')

        ax.set_xlabel('X(t)')
        ax.set_xlim3d((min(x)+0.1*min(x), max(x)+0.1*max(x)))
        ax.set_ylabel('Y(t)')
        ax.set_ylim3d((min(y)+0.1*min(y), max(y)+0.1*max(y)))
        ax.set_zlabel('Z(t)')
        ax.set_zlim3d((min(z)+0.1*min(z), max(z)+0.1*max(z)))
        ax.set_title('3D Discretised Brownian Paths')

        ### Use list comprehension to create a list of Line2D Objects
        lines = [ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1])[0] for data in walkData]

        ### Create animation object using the FuncAnimation() method
        anim = animation.FuncAnimation(
            fig, self.update_random_walks, N+1, fargs=(walkData, lines, '3D'), interval=30, repeat=True, blit=False)

        plt.show()


if __name__ == '__main__':
    ### Create instance of class and call relevant method
    test = BrownianAnimation()
    test.animate('3D')