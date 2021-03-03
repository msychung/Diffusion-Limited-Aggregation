# Notes
*Week 18 progress update:* took the last week or so off because I had a hectic week of job interviews/assessment centres. Now full steam ahead. 

### Animation (brownian_animation.py)
- [x] Combine 1D, 2D, 3D animation methods into one single method with dimension parameter
- [ ] Decide whether you want one big animation method (with dimension parameter) or individual 1D, 2D, 3D animation methods - ask?

### Brownian Motion (brownian_prototype.py)
- [x] Replace for loop with vectorised method? Is much quicker and probably neater
  ```
  dx = np.sqrt(dt) * np.random.randn(1,N)
  x = np.cumsum(ds, axis=1)
  ```
  - All elements of dx are generated at once through creating an array of size 1 x N (should be size M x N for multiple 1D paths)
  - np.cumsum() returns cumulative sum of elements of dx

- [x] Extend to 3D

- [x] Extend to multiple paths (for all dimensions)

- [ ] Could test for the mean free time $\tau$, the time interval between collisions (or steps). $\tau$ = T/N where N is the total number
of steps and T is the total time.
