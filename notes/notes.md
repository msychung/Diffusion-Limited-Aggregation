# NOTES

### Brownian Motion
- Replace for loop with vectorised method? Is much quicker and probably neater
```
dX = np.sqrt(dt) * np.random.randn(1,N)
X = np.cumsum(dX, axis=1)
