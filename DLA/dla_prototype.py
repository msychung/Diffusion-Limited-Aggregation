import random
import math
import numpy as np
import pygame


class Particle():
    '''Component class used to ...'''
    def __init__(self, x, y):
        '''
        .

        Parameters
        ----------
        x : int
            The horizontal pixel position...
        y : int
            The vertical pixel position... 
        '''
        self.x = x
        self.y = y
    

    def update(self, x, y):
        '''
        .

        Parameters
        ----------
        x : int
            The horizontal pixel position...                   
        y : int
            The vertical pixel position... 
        '''
        self.x = x
        self.y = y
        


class Application():
    '''Composite class used to run the main DLA simulation in 2D. Takes in the Particle class as a component, to generate many particles through repeated instantiation. Generates an animation of Brownian tree (DLA cluster) formation using pygame.'''

    def __init__(self, n, seed_shape, spawn_shape, padSize, crystal_size_limit, view=False):
        '''
        Initialises all class attributes and creates n particles based on the Particle class. Calls the on_execute() method to run the simulation.

        Parameters
        ----------
        n : int
            The total number of particles in the simulation
        seed_shape : str
            The shape of the seed to which particle aggregate
        spawn_shape : str
            The shape from which particles randomly spawn 
        padSize : int
            The size of the spawn shape
        crystal_size_limit : int
            The maximum size of the DLA cluster allowed before the simulation exits
        view : bool
            Whether or not individual particle motion is viewed along with the growing DLA cluster
        '''
        ### Raise an exception if the input spawn_shape parameter is invalid
        if spawn_shape != 'square' and spawn_shape != 'circle':
            raise Exception('Parameter "spawn_shape" must be "square" or "circle".')
 
        ### Initialise display surface, set its size and initialise pixel array and colour
        self.size = self.width, self.height = 800, 600      # size of display screen
        self.crystalColor = 0xDCDCDC     # grey in hex
        self.n = n
        self.view = view
        
        ### Set seed and spawn shapes (taken in as input parameters)
        self.seed_shape = seed_shape
        self.spawn_shape = spawn_shape

        ### Set centre co-ordinates
        self.start_x = round(self.width/2)
        self.start_y = round(self.height/2)  

        ### Define square domain size in pixels
        self.padSize = padSize
        
        ### Define a square domain that is padSize pixels larger than crystal domain
        self.sqdomainMin_x = self.start_x - self.padSize
        self.sqdomainMax_x = self.start_x + self.padSize
        self.sqdomainMin_y = self.start_y - self.padSize
        self.sqdomainMax_y = self.start_y + self.padSize

        ### Define circle domain radius in pixels
        self.radius = padSize

        ### Set a size limit for the growing crystal
        self.crystal_size_limit = crystal_size_limit

        ### Set a sticking coefficient, describing the probability a particle will stick to the cluster
        self.stick_coeff = 0.8
        
        ### Create an empty list to store all the particle objects created below
        self.all_particles = []

        ### Use composition to create n particle instances using the Particle class.
        # *self.square_spawn() = x, y is a keyword argument
        for i in range(n):
            if self.spawn_shape == 'square':
                particle = Particle(*self.square_spawn())

            elif self.spawn_shape == 'circle':
                particle = Particle(*self.circle_spawn())

            self.all_particles.append(particle)

        ### Create an empty list to store the positions (x and y) of the pixels forming the growing cluster
        self.crystal_position = []

        ### Initialise min and max x, y to define a rectangular cluster domain (limits of cluster)
        self.min_x, self.min_y = self.start_x, self.start_y
        self.max_x, self.max_y = self.start_x, self.start_y

        ### Call the main on_execute() method
        self.on_execute()


    def on_init(self):
        '''Initialises pygame attributes.'''

        pygame.init()   # Initialise pygame
        pygame.display.set_caption("2D Diffusion Limited Aggregation")      # Window title

        self.displaySurface = pygame.display.set_mode(self.size)      # Create display surface
        self.pixelArray = pygame.PixelArray(self.displaySurface)      # Create pixel array
        self.start_time = pygame.time.get_ticks()                     # Set a timer

        ### Generate a seed based on self.seed_shape and set the self.isRunning flag to True
        self.gen_seed()
        self.isRunning = True
    

    def on_event(self, event):
        '''
        Called during main on_execute() loop which loops over all events continuously during the simulation.

        Parameters
        ----------
        event : object
            A pygame event
        '''
        ### In the event we want to quit the game, print the total time elapsed and quit
        if event.type == pygame.QUIT:
            time = pygame.time.get_ticks() - self.start_time
            print("A total of", time/1000, "seconds has elapsed.")
            self.isRunning = False


    def gen_seed(self):
        '''Creates a seed of a specified seed shape. Raises an exception for invalid seed inputs.'''

        if self.seed_shape == 'dot':
            self.pixelArray[self.start_x, self.start_y] = self.crystalColor

        elif self.seed_shape == 'line':
            pygame.draw.line(self.displaySurface, self.crystalColor, (self.start_x-50, self.start_y), (self.start_x+50, self.start_y))

        elif self.seed_shape == 'circle':
            pygame.draw.circle(self.displaySurface, self.crystalColor, (self.start_x, self.start_y), 30, width=1)

        elif self.seed_shape == 'ellipse':
            pygame.draw.ellipse(self.displaySurface, self.crystalColor, ((self.start_x, self.start_y), (32, 20)), width = 1)

        elif self.seed_shape == 'square':
            pygame.draw.rect(self.displaySurface, self.crystalColor, ((self.start_x, self.start_y), (50, 50)), width = 1)

        elif self.seed_shape == 'star':   # because my dad asked me to!
            x = self.start_x
            y = self.start_y
            star_points  = [(x, y-76), (x+20, y-25), (x+73, y-28), (x+28, y+5), (x+42, y+55), (x, y+23), (x-42, y+55), (x-28, y+5), (x-73, y-28), (x-20, y-25)]
            pygame.draw.polygon(self.displaySurface, self.crystalColor, star_points)
        
        else:
            raise Exception("Invalid seed shape, please enter either 'dot', 'line', 'circle', 'ellipse', 'square' or 'star'.")


    def square_spawn(self):
        '''
        Randomly choose a position on a side of a square for a particle to spawn along.

        Returns
        -------
        x : int
            The horizontal pixel position along the square from which the particle will spawn
        y : int
            The vertical pixel position along the square from which the particle will spawn 
        '''
        ### Denote each side of a square as sides 1, 2, 3 or 4. 
        newSide = random.choice([1, 2, 3, 4])

        ### Generates particles uniformly along any one edge.
        if newSide == 1:
            x = self.sqdomainMin_x
            y = int(random.uniform(self.sqdomainMin_y, self.sqdomainMax_y))

        elif newSide == 2:
            x = int(random.uniform(self.sqdomainMin_x, self.sqdomainMax_x))
            y = self.sqdomainMin_y

        elif newSide == 3:
            x = self.sqdomainMax_x
            y = int(random.uniform(self.sqdomainMin_y, self.sqdomainMax_y))

        else:   # newSide == 4
            x = int(random.uniform(self.sqdomainMin_x, self.sqdomainMax_x))
            y = self.sqdomainMax_y
        
        return x, y


    def circle_spawn(self):
        '''
        Randomly choose a position on a circle of radius self.radius for the particle to spawn on.
        
        Returns
        -------
        x : int
            The horizontal pixel position along the circle from which the particle will spawn
        y : int
            The vertical pixel position along the circle from which the particle will spawn 
        '''
        ### Choose a random angle theta
        theta = random.random() * 2 * math.pi

        ### Generate x and y co-ordinates based on this theta and the specified radius
        x = int(self.start_x + math.cos(theta)*self.radius)
        y = int(self.start_y + math.sin(theta)*self.radius)

        return x, y


    def on_loop(self):
        '''
        Loops around each of the n particles and updates positions by one step.
        '''
        ss = 1    # Set step size of paricles

        ### Recolour existing (and growing) crystal each loop iteration, only if self.view == True
        if self.view:
            for coordinate in self.crystal_position:
                self.pixelArray[coordinate[0], coordinate[1]] = self.crystalColor

        ### Loop over all particles 
        for particle in self.all_particles:
            # Eightfold direction on a square pixel lattice, with no bias
            (dx, dy) = random.choice([(0, ss), (0, -ss), (ss, 0), (-ss, 0), (ss, -ss), (-ss, ss), (ss, ss), (-ss, -ss)])

            # Assign increments to new x and y variables to keep a record of current and future position
            new_x = particle.x + dx
            new_y = particle.y + dy

            # Call wrap_around method to wrap around movement around based on a chosen domain shape
            new_x, new_y = self.wrap_around(particle, new_x, new_y)
            
            # Check if pixel has already been covered by walker 
            if self.pixelArray[new_x, new_y] == self.crystalColor and random.random() <= self.stick_coeff:  
                # Set pixel to same colour as growing crystal and append to crystal_position list
                self.pixelArray[particle.x, particle.y] = self.crystalColor
                self.crystal_position.append((particle.x, particle.y))

                # Calculate the distance between the particle (newest addition to the DLA crystal) and the seed centre
                x = particle.x - self.start_x
                y = particle.y - self.start_y
                distance = math.sqrt(x**2 + y**2)

                # Quit the simulation if the crystal size exceeds the specified limit, and print the total time elapsed
                if distance > self.crystal_size_limit:
                    time = pygame.time.get_ticks() - self.start_time
                    print("A total of", time/1000, "seconds has elapsed.")
                    self.isRunning = False
                    return

                # Modify simulation domain as crystal grows
                if particle.x < self.min_x:
                    self.min_x = particle.x

                elif particle.x > self.max_x:
                    self.max_x = particle.x

                if particle.y < self.min_y:
                    self.min_y = particle.y
                    
                elif particle.y > self.max_y:
                    self.max_y = particle.y
                    
                self.restrict_domain()

                # Respawn the particle once it has adhered to the crystal
                if self.spawn_shape == 'square':
                    particle.update(*self.square_spawn())
                
                elif self.spawn_shape == 'circle':
                    particle.update(*self.circle_spawn())

            else:
                ### Otherwise move the particle to the new position
                particle.x, particle.y = new_x, new_y

                ### Show individual particles moving in green, only if self.view == True
                if self.view:
                    self.pixelArray[particle.x, particle.y] = 0x00FF00   # green in hex
                
        # Update the display window
        pygame.display.update()

        # Remove previous particle paths, only for viewing purposes of individual particles
        if self.all_particles and self.view:
            self.displaySurface.fill((0,0,0,))      # Removes previous path of particles


    def wrap_around(self, particle, new_x, new_y):
        '''
        Ensures any random walk does not disappear off the screen, otherwise application quits (breaks). 
        Improves computational performance by wrapping the particle around to the other side of the domain.

        Parameters
        ----------
        particle : object
            An object of the Particle class representing an individual particle
        new_x : int
            Original pixel number of the horizontal position to which the particle will go
        new_y : int
            Original pixel number of the horizontal position to which the particle will go

        Returns
        -------
        new_x : int
            New pixel number of the horizontal position to which the particle will go

        new_y : int
            New pixel number of the vertical position to which the particle will go
        '''
        ### Wrap-around for a square domain
        if self.spawn_shape == 'square':
            if new_x < self.sqdomainMin_x:
                new_x = self.sqdomainMax_x
            if new_x > self.sqdomainMax_x:
                new_x = self.sqdomainMin_x
            if new_y < self.sqdomainMin_y:
                new_y = self.sqdomainMax_y
            if new_y > self.sqdomainMax_y:
                new_y = self.sqdomainMin_y
    
        ### Wrap-around for a circular domain
        elif self.spawn_shape == 'circle':
            sqx = (new_x - self.start_x)**2
            sqy = (new_y - self.start_y)**2
            r = math.sqrt(sqx + sqy)
            
            if r > self.radius:
                new_x = -particle.x
                new_y = -particle.y
        
        return new_x, new_y


    def restrict_domain(self):
        '''Ensures domain minima and maxima never extend beyond the screen boundaries, otherwise application quits (breaks) prematurely. Also allows the simulation domain to expand with growth of the DLA cluster to maintain computational performance.'''

        ### Domain restrictions for a square spawn
        if self.spawn_shape == 'square':
            self.sqdomainMin_x = max([self.min_x - self.padSize, 1])
            self.sqdomainMax_x = min([self.max_x + self.padSize, self.width - 1])
            self.sqdomainMin_y = max([self.min_y - self.padSize, 1])
            self.sqdomainMax_y = min([self.max_y + self.padSize, self.width - 1])

        ### Domain restrictions for a circular spawn
        elif self.spawn_shape == 'circle':
            max_radius = 0

            for pixel in self.crystal_position:
                x = pixel[0] - self.start_x
                y = pixel[1] - self.start_y
                radius = np.sqrt(x**2 + y**2)

                if radius > max_radius:
                    max_radius = radius

            self.radius = max_radius + self.padSize


    def on_execute(self):
        '''Method called when application is first run. Executes the simulation for as long as self.isRunning == True.'''
        ### Call the pygame constructor method (initialises pygame)
        self.on_init()
      
        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()

        pygame.quit()


# Prevents this test object instantiating when running the file externally (i.e. from frac_dim.py)
if __name__ == '__main__':
    ### Form: Application(n, seed_shape, spawn_shape, padSize, crystal_size_limit, view=False)
    test = Application(1000, 'dot', 'circle', 50, 200)