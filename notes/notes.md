# Notes

### Brownian Motion
- Replace for loop with vectorised method? Is much quicker and probably neater
  ```
  dx = np.sqrt(dt) * np.random.randn(1,N)
  x = np.cumsum(ds, axis=1)
  ```
  - All elements of dx are generated at once through creating an array of size 1 x N (should be size M x N for multiple 1D paths)
  - np.cumsum() returns cumulative sum of elements of dx
