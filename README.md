<p align="center">
  <img src="https://www.lancaster.ac.uk/media/lancaster-university/content-assets/images/fst/logos/Physicslogo.svg" width="350" height="95">
</p>

## PHYS 389 Computer Modelling Project

This repository contains all code developed for the PHYS 389 Computer Modelling Project at Lancaster University. The course involves a further development of scientific modelling skills in Python, through the implementation of numerical algorithms in a selected physical system. A core focus is on thorough testing and debugging of software to ensure its robustness, combined with careful planning and design of an open-ended project. An understanding of OOP will be extended, and advanced data visualisation and analysis techniques will be explored. 

I have chosen to model 2D diffusion-limited aggregation (DLA), a process involving the aggregation, or clustering, of particles undergoing Brownian motion. When such particles are allowed to adhere to a seed point, clusters (Brownian trees) are formed with distinct tree-like shapes. This is a demonstration of fractal geometry at play in the natural world, finding many practical applications in science from electrochemical deposition to snowflake formation.

The fundamental basis of the model involves a particle being introduced into a system at a random position, before undergoing a random walk until it encounters an existing DLA structure. This will initially be a single stationary 'seed' particle, but upon contact the particle will permanently adhere to the seed, becoming part of the DLA cluster. The growing aggregate results in the formation of so-called 'Brownian trees'.

Examples of this process can be seen below: 

*insert gifs*

### Structure & Design
The two code-containing folders in this repository are [**random-processes**](https://github.com/Lancaster-Physics-Phys389-2021/phys389-2021-project-msychung/tree/main/random-processes) and [**DLA**](https://github.com/Lancaster-Physics-Phys389-2021/phys389-2021-project-msychung/tree/main/DLA). 

**random-processes** contains `constantstep.py`, `variablestep.py` and `langevin.py`. The first two simulate simple random walks in 1D, 2D and 3D, with either fixed or variable step size, whilst the latter attempts to solve the Langevin equation using *scipy.integrate.solve_ivp*. This last file was ultimately not explored further. 

**DLA** contains `dla_simulation.py` and `frac_dim.py`, which run the main simulation for 2D DLA and its analysis respectively. 

Thus the detailed functionality of the 4 main files in this program are:
 - `constant_step.py`
 Generates and plots random walks in 1D, 2D and 3D with fixed step size, using *random.choice*. Calculates average and rms displacements over many walk iterations, then plots distance of a particle as a function of steps taken away from the start point. All plots are created using *matplotlib*.
 -  `variable_step.py`
 Extends the 1D, 2D and 3D random walks of constantstep.py to variable step size and multiple particles. Uses *numpy.random.randn* to vary step size based on the standard Gaussian distribution, and display walks for multiple particles on the same plot. Average displacement over many walk iterations is calculated. Animations are also created for multiple particles at the same time, using *matplotlib.animation*. Positional and time data is stored in a *pandas* DataFrame, for ease of plotting and animation.
 -  `dla_simulation.py`
 Simulates the formation of a Brownian tree by DLA in 2D. Uses *pygame* to implement an animation of particle aggregation to a central seed, as described above. Usage of composition allows a class hierarchy to form, with a composite class Application and a component class Particle. This allows implementation of many-particle trajectories simultaneously, through instantiation of the Particle class within a loop. The main Application class initialises all relevant attributes, before creating a seed under a determined spawn shape, and then updating the positions of n particles sequentially. The direction of each step increment is implemented using *random.choice*, with no bias applied in any one direction. The DLA clusters freely grow until they reach a specified size limit, upon which the simulation ends.
 -  `frac_dim.py`
Calculates the Hausdorff dimension D_h for a 2D DLA cluster. Extended to iterate calculations over many DLA cluster radii, allowing a more accurate D_h value to be obtained. Uses *matplotlib* to generate plots of ln(mass) against ln(radius) with best fit straight lines, to visualise the distribution of data points across a wide range of mass and radius values. Data for the calculations and plots is stored and saved in *pandas* DataFrames.

There are additionally unit test files (denoted *test_filename*) for all main code files, written in *pytest*. 

Finally, there are folders for [**ideas**](https://github.com/Lancaster-Physics-Phys389-2021/phys389-2021-project-msychung/tree/main/ideas) and [**notes**](https://github.com/Lancaster-Physics-Phys389-2021/phys389-2021-project-msychung/tree/main/notes), which contain documentation and markdown notes relevant to the development and submission of the project.

### Prerequisites, Installation & Usage
Ensure you have the following prerequisites on your development machine:
* Python - [Download & Install Python](https://www.python.org/downloads/). Ensure Python 3 is installed (not Python 2), and that you install for the correct OS
* Command Line or an IDE/Text Editor like [VSCode](https://code.visualstudio.com/)

The following Python packages will also require installation before use of the software:
- `random`
- `numpy`
- `scipy`
- `pandas`
- `matplotlib`
- `cycler`
- `pygame`
- `pytest`

Package installation is carried out in the command line, a text interface which takes in user commands and passes them to a device's operating system.
To install a package, enter the following in the command line:
```
> python -m pip install module-name
```
where `module-name` is the name of the module, e.g. `matplotlib`, `scikit-image`. These modules can all be entered in the same line, separated by spaces. 

If you have previously installed any of these packages, ensure you update to the most recent release via:
```
> pip install --upgrade module-name
```
You can also view a list of all installed python packages using `pip list`. 

Although not optimised for user configuration, each file should produce relevant results when run. This may not be immediate, as relevant parameters may need to be changed manually, or in some cases lines may require commenting out to run certain functions and not others. The specifics should be documented within each file. 

Note that test files (denoted `test_filename`) are not run in the conventional way, but instead require calling pytest in the command line: `pytest test_filename`. 

### Built With
* [Python 3.9.2](https://github.com/python/cpython)
  * [random](https://docs.python.org/3/library/random.html)
  * [numpy](https://numpy.org/), including [numpy.random](https://numpy.org/doc/1.16/reference/routines.random.html)
  * [pandas](https://pandas.pydata.org/)
  * [matplotlib](https://matplotlib.org/), including [matplotlib.animation](https://matplotlib.org/stable/api/animation_api.html)
  * [pygame](https://www.pygame.org/wiki/about)

### Contributing
All contributions towards this simulation are welcome. I aim to review any contributions on a semi-periodic basis, depending on future day-job workload.

To contribute using version control software (Git):
1) Create a new branch (and fork if applicable), labelling it appropriately
2) Make the changes on that branch
3) Commit to and push the changes
4) Create a pull request from your branch to master
5) I will then review your pull request

Please try to adhere to [PEP8](https://www.python.org/dev/peps/pep-0008/) style. My attempt at doing so is not perfect, but readability to a satisfactory level is key!

### License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT "Open Source MIT"). This license is conducive to free, open-source software.
