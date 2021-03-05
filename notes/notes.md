# Notes
*Week 18 progress update:* took the last week or so off because I had a hectic week of job interviews/assessment centres. Now full steam ahead. 
## Random Walks
### Constant step size
#### Prototype (constantstep_prototype.py)
- [x] Produce 1D random walk and extend to 2D and 3D

- [x] Produce plots of paths

- [ ] Decide if it's worth animating (probably not)

- [x] Calculate average displacements for all dimensions

##### TESTS
- [ ] Test consistency when changing step size (e.g. 1 to 2, fractional) and introducing bias - do displacements adjust accordingly?

- [ ] Test whether 1D/2D lattice walks are recurrent (return to starting point is certain), and >3D are transient (return to starting point is uncertain)


##### NOTES FOR REFERENCE
- Even steps should result in displacements closer to the starting point (origin) than odd steps, since odd steps result in one more step in a given direction than any other. 

### Variable step size
#### Animation (variablestep_anim.py)
This file visualises the 1D, 2D and 3D random walk results through animations. 

##### TO DO
- [x] Combine 1D, 2D, 3D animation methods into one single method with dimension parameter

- [ ] Decide whether you want one big animation method (with dimension parameter) or individual 1D, 2D, 3D animation methods - ask?

#### Prototype (variable step_prototype.py)
This file performs the following:
- imports the relevant modules
- initialises the method attributes (maybe turn common ones in class attributes?)
- generates the random walks
- generates plots (maybe move to animation
- calculates average displacements and mean free time for each walk
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
- [ ] Average displacement <d> after N steps should be 0

- [ ] Root-mean-square disciplacement after N steps should be sqrt(N)

- [ ] Could test for the mean free time $\tau$, the time interval between collisions (or steps). $\tau$ = T/N where N is the total number of steps and T is the total time.

##### NOTES FOR REFERENCE
- You need to refresh your stats lol, standard normal distribution isn't between -1 and 1!!

- Vectorised method is more efficient since all elements dx are generated at once (using numpy.random.randn), instead of generating one at a time using the for loop method

- Using a seed for reproducibility is basically essential for further analysis later on - needed for testing

