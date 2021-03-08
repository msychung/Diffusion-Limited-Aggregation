import math
import numpy as np
from numpy import random
import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler
from scipy.integrate import odeint, solve_ivp
plt.style.use('seaborn-whitegrid')


def OU_process():
    '''
    Solve the Langevin equation (describes time evolution of Brownian motion) using the Ornstein-Uhlenbeck process and the Euler-Maruyama method.
    '''

    mu = 10.0    # mean
    sigma = 1.0    # standard deviation
    tau = 0.05   # time constant (mean free time)

    T = 1.0    # total time
    dt = 0.001   # time step
    n = int(T/dt)    # number of time steps
    t = np.linspace(0.0, T, n)    # create time list (from 0 to T with step size T/N)

    x = np.zeros(n)     # create array to hold x values

    ### Define renormalised variables
    sigma_bis = sigma * np.sqrt(2.0/tau)
    sqrtdt = np.sqrt(dt)

    ### Implement the Euler-Maruyama method
    for i in range(n - 1):
        x[i+1] = x[i] + dt*(-(x[i] - mu) / tau) + (sigma_bis * sqrtdt * np.random.randn())

    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(t, x, lw=2)
    plt.show()


    ### Calculate estimated distribution 
    ntrials = 10000
    X = np.zeros(ntrials)

    ### Create bins for the histograms.
    bins = np.linspace(-2., 14., 100)
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))

    for i in range(n):
        # Update the process independently for all trials
        X += dt * (-(X - mu) / tau) + \
            sigma_bis * sqrtdt * np.random.randn(ntrials)

        # Display the histogram for various points in time
        if i in (5, 50, 500):
            hist, _ = np.histogram(X, bins=bins)
            ax.plot((bins[1:] + bins[:-1]) / 2, hist,
                    {5: '-', 50: '.', 500: '-.', }[i],
                    label=f"t={i * dt:.2f}")

        ax.legend()
    plt.show()


def langevin(t, inicon):

  m = 1.5 
  k = 0.000001
  R = np.random.normal(0,1) 

  x0 = inicon[0]
  v0 = inicon[1]

  dvdt = -m*v0 + k*R

  return [v0, dvdt]   # returns v0 as x_n+1 

t = np.linspace(0, 1000, 1000000)

output = solve_ivp(langevin, [0, 1000], [0, 1], t_eval=t, method='RK45')

fig, ax = plt.figure(), plt.axes()
ax.plot(t, output.y[0])
ax.plot(t, output.y[1])
plt.show()

### Call function
# OU_process()
