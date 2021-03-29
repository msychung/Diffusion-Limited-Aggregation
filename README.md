<p align="center">
  <img src="https://www.lancaster.ac.uk/media/lancaster-university/content-assets/images/fst/logos/Physicslogo.svg" width="350" height="95">
</p>

## PHYS 389 Computer Modelling Project

This repository contains all code developed for the PHYS 389 Computer Modelling Project at Lancaster University. The course involves a further development of scientific modelling skills in Python, through the implementation of numerical algorithms in a selected physical system. A core focus is on thorough testing and debugging of software to ensure its robustness, combined with careful planning and design of an open-ended project. An understanding of OOP will be extended, and advanced data visualisation and analysis techniques will be explored. 

I have chosen to model 2D diffusion-limited aggregation (DLA), a process involving the aggregation, or clustering, of particles undergoing Brownian motion. When such particles are allowed to adhere to a seed point, clusters (Brownian trees) are formed with distinct tree-like shapes. This is a demonstration of fractal geometry at play in the natural world, finding many practical applications in science from electrochemical deposition to snowflake formation.

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

Please try to adhere to [PEP8](https://www.python.org/dev/peps/pep-0008/) style https://www.python.org/dev/peps/pep-0008/convention. My attempt at doing so is not perfect, but readability to a satisfactory level is key!

### License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT "Open Source MIT"). This license is conducive to free, open-source software.

---
To add:
- [ ] An outline of my chosen physical system 
- [x] 'Prerequisites, installation & usage' sections
- [x] 'Built with' section (once you know which packages you are using)
- [x] 'Contribution' section
- [ ] Insert picture/gif of simulation once completed
