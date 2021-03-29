import math
import numpy as np
import pandas as pd
from dla_prototype import Application
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

class Fractal_Dimension():
    '''
    Calculates the Hausdorff dimension H_d of a 2D DLA cluster and plots a log-log mass vs. radius graph 
    '''

    def __init__(self):
        '''
        Adjust parameters accordingly and set range of for loop to determine number of iterations
        '''
        self.clusters = [Application(200, 'dot', 'circle', 50, 40, run) for run in range(2, 180, 2)]
        

    def cluster_mass(self):
        '''
        Calculates the 'mass' of the DLA cluster by counting the number of particles (pixels). 

        Parameters
        ----------
        None

        Returns
        -------
        mass_list : list
            List containing the total mass of each cluster in self.clusters
            
        logMass_list : list
            List containing the ln(value) of each element in mass_list
        '''
        mass_list = []
        logMass_list = []
        time_list = []

        for cluster in self.clusters:
            mass = len(cluster.crystal_position)
            mass_list.append(mass)

            logMass = np.log(mass)
            logMass_list.append(logMass)

        return mass_list, logMass_list
        

    def cluster_radius(self):
        '''
        Calculates the 'radius of gyration' of the DLA cluster based on a list of pixel positions

        Parameters
        ----------
        None

        Returns
        -------
        max_radius_list : list
            List containing the maximum obtained radius of each cluster in self.clusters

        logRadius_list: list
            List containing the ln(value) of each element in max_radius_list
        '''
        max_radius_list = []
        logRadius_list = []

        for cluster in self.clusters:
            max_radius = 0
            for pixel in cluster.crystal_position:
                x = pixel[0] - cluster.start_x
                y = pixel[1] - cluster.start_y
                radius = np.sqrt(x**2 + y**2)
            
                if radius > max_radius:
                    max_radius = radius

            logRadius = np.log(math.floor(max_radius))
            max_radius_list.append(math.floor(max_radius))
            logRadius_list.append(logRadius)

        return max_radius_list, logRadius_list


def print_save_results(test):
    '''
    Prints the lists of interests (optional) and creates a pandas DataFrame to store and save lists.
    '''
    mass_list, logMass_list = test.cluster_mass()
    max_radius_list, logRadius_list = test.cluster_radius()
    # print("List of N: ", mass_list)
    # print("List of ln(mass): ", logMass_list)
    # print("List of crystal radii: ", max_radius_list)
    # print("List of ln(radius): ", logRadius_list)

    df = pd.DataFrame({'mass': mass_list, 'radius': max_radius_list, 'ln(mass)': logMass_list, 'ln(radius)': logRadius_list})
    # df.to_pickle("Fractal Dimension Circle")

    print(df.head)


def plot_frac_dim():
    '''
    Plots the relevant columns of the pandas DataFrame along with the best linear fit to data

    Parameters
    ----------
    None

    Returns
    -------
    slope : float
        The slope of the log-log plot, representing the value of the Hausdorff dimension H_d
    '''
    df = pd.read_pickle("Fractal Dimension Square")
    logRadius_list = np.log(df['radius'])
    df['ln(radius)2'] = logRadius_list
    df = df.iloc[:-25]

    slope, intercept = np.polyfit(df['ln(radius)2'], df['ln(mass)'], 1)  # Create a least squares polynomial fit 
    slope_func = np.poly1d(slope)

    ### Plot ln(mass) against ln(radius)
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(df['ln(radius)2'], df['ln(mass)'], marker='o', markersize=1.5, linewidth=0)
    ax.plot(df['ln(radius)2'], slope*df['ln(radius)2'] + intercept, color='dodgerblue', linewidth=0.5)
    
    ax.set_xlabel('ln(radius)')
    ax.set_ylabel('ln(mass)')
    ax.title.set_text('Log-log plot of DLA crystal mass against radius')

    plt.show()

    return slope


if __name__ == '__main__':
    # test = Fractal_Dimension()
    # print_save_results(test)

    # df = pd.read_pickle("Fractal Dimension Circle")
    # print(df.head)

    # slope = plot_frac_dim()
    # print(slope)