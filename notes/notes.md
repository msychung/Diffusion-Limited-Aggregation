# Notes
*Week 18 progress update:* took the last week or so off because I had a hectic week of job interviews/assessment centres. Now full steam ahead. 

## Random Walks
### Constant step size
#### Prototype (constantstep_prototype.py)
This file performs the following:
- imports the relevant modules
- initialises the class attribute butes?)
- generates the random walks
- generates plots 
- calculates average displacements for each walk
- displays gathered information

##### TO DO
- [x] Produce 1D random walk and extend to 2D and 3D

- [x] Produce plots of paths

- [x] Decide if it's worth animating (decided it's not)

- [x] Calculate average displacements for all dimensions

##### TESTS
- [x] Average displacement <d> after N steps should be 0

- [x] Root-mean-square disciplacement after N steps should be sqrt(N)

- [x] Test consistency when changing step size (e.g. 1 to 2, fractional) and introducing bias - do displacements adjust accordingly?

##### NOTES FOR REFERENCE
- Even steps should result in displacements closer to the starting point (origin) than odd steps, since odd steps result in one more step in a given direction than any other. 

- Changing step size to a fixed number (inc. fractions) other than 1 changes rms displacement proportionally, and average <d> remains close to zero.

- Introducing bias results in completely skewed mean and rms displaements (as expected).

- 1D/2D lattice walks are recurrent (return to starting point is certain), and >3D are transient (return to starting point is uncertain). Testing this recurrence/transience is difficult for a computer simulation 

### Variable step size
#### Animation (variablestep_anim.py)
This file visualises the 1D, 2D and 3D random walk results through animations. 

##### TO DO
- [x] Combine 1D, 2D, 3D animation methods into one single method with dimension parameter

- [ ] Decide whether you want one big animation method (with dimension parameter) or individual 1D, 2D, 3D animation methods - ask?

#### Prototype (variable step_prototype.py)
This file performs the following:
- imports the relevant modules
- initialises the class attributes
- generates the random walks
- generates plots **(maybe move to animation)**
- displays gathered information

##### TO DO
- [x] Replace for loop with vectorised method? Is much quicker and probably neater
  ```
  dx = np.sqrt(dt) * np.random.randn(1,N)
  x = np.cumsum(ds, axis=1)
  ```
  - All elements of dx are generated at once through creating an array of size 1 x N (should be size M x N for multiple 1D paths)
  - np.cumsum() returns cumulative sum of elements of dx

- [x] Extend to 3D

- [x] Extend to multiple paths (for all dimensions)

- [ ] Calculate average displacements at each step (to plot a graph, instead of just final displacement)

##### TESTS
- [x] Average displacement <d> after N steps should be 0

- [x] Root-mean-square disciplacement after N steps should NOT be sqrt(N) due to variable step size - need to use a PDF i.e. continuous variable -> Langevin equation! 

- [ ] Could test for the mean free time $\tau$, the time interval between collisions (or steps). $\tau$ = T/N where N is the total number of steps and T is the total time. Not really sure if I can test this since it's just a calculation...

##### NOTES FOR REFERENCE
- You need to refresh your stats lol, standard normal distribution isn't between -1 and 1!!

- Vectorised method is more efficient since all elements dx are generated at once (using numpy.random.randn), instead of generating one at a time using the for loop method

- Using a seed for reproducibility is basically essential for further analysis later on - needed for testing


## Brownian Motion
### Langevin Equation (langevin.py)
Solving the Langevin equation, a continuous stochastic differential equation describing the time evolution of Brownian motion.

##### TO DO
- [ ] Experiment with solving using the Ornstein-Uhlenbeck process and the Euler-Maruyama method.

- [ ] Experiment with using the scipy.integrate.solve_ivp package 

## DLA
### Prototype (dla_prototype.py)
Simulating 2D Diffusion Limited Aggregation (DLA) using pygame.

##### TO DO
- [x] Simulate 2D random walks (no seed) in pygame

- [x] Add a seed point 

- [x] Show motion of all particles without motion history

- [ ] Introduce different seed and domain shapes

- [ ] Automate image capture and saving at a specified point of the simulation

### Fractal Dimension (frac_dim.py)
Calculating the fractal dimension of a DLA image using the Minkowski–Bouligand (box-counting) dimension.
