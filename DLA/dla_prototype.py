import random
import math
import numpy as np
import pygame

class Particle():

    def __init__(self, spawn_shape, sqdomainMin_x, sqdomainMax_x, sqdomainMin_y, sqdomainMax_y, start_x, start_y, radius):
        # Choose a spawn shape
        if spawn_shape == 'square':
            self.spawn_shape = self.square_spawn
            self.square_spawn(sqdomainMin_x, sqdomainMax_x, sqdomainMin_y, sqdomainMax_y, start_x, start_y, radius)

        elif spawn_shape == 'circle':
            self.spawn_shape = self.circle_spawn
            self.circle_spawn(sqdomainMin_x, sqdomainMax_x, sqdomainMin_y, sqdomainMax_y, start_x, start_y, radius)

    def square_spawn(self, sqdomainMin_x, sqdomainMax_x, sqdomainMin_y, sqdomainMax_y, start_x, start_y, radius):
        # Randomly choose a position on a side of a square for a particle to spawn along
        newSide = random.choice([1, 2, 3, 4])
        if newSide == 1:
            self.x = sqdomainMin_x
            self.y = int(random.uniform(sqdomainMin_y, sqdomainMax_y))
        elif newSide == 2:
            self.x = int(random.uniform(sqdomainMin_x, sqdomainMax_x))
            self.y = sqdomainMin_y
        elif newSide == 3:
            self.x = sqdomainMax_x
            self.y = int(random.uniform(sqdomainMin_y, sqdomainMax_y))
        else:   # newSide == 4
            self.x = int(random.uniform(sqdomainMin_x, sqdomainMax_x))
            self.y = sqdomainMax_y

    def circle_spawn(self, sqdomainMin_x, sqdomainMax_x, sqdomainMin_y, sqdomainMax_y, start_x, start_y, radius):
        # Randomly choose a position on a circle of radius r for the particle to spawn on
        x0, y0 = start_x, start_y
        r = radius

        theta = random.random() * 2 * math.pi
        self.x = int(x0 + math.cos(theta)*r)
        self.y = int(y0 + math.sin(theta)*r)


class Application():

    def __init__(self, n):
        # Initialise display surface, set its size and initialise pixel array and colour
        self.displaySurface = None
        self.size = self.width, self.height = 640, 360      # size of display screen
        self.pixelArray = None
        self.crystalColor = 0xDCDCDC        # grey
        self.n = n
        
        # Set seed, spawn and domain shapes
        self.seed_shape = 'dot'
        self.spawn_shape = 'square'
        self.domain_shape = 'square'

        # Set centre co-ordinates
        self.start_x = round(self.width/2)
        self.start_y = round(self.height/2)  

        self.updateFlag = False
        self.padSize = 20
        
        # Define a square domain that is padSize pixels larger than crystal domain
        self.sqdomainMin_x = self.start_x - self.padSize
        self.sqdomainMax_x = self.start_x + self.padSize
        self.sqdomainMin_y = self.start_y - self.padSize
        self.sqdomainMax_y = self.start_y + self.padSize

        # Define circle domain radius in pixels
        self.radius = 80

        self.crystal_size_limit = 30

        # Use composition to create n particle instances using the Particle class
        self.all_particles = []
        for i in range(n):
            particle = Particle(self.spawn_shape, self.sqdomainMin_x, self.sqdomainMax_x, self.sqdomainMin_y, self.sqdomainMax_y, self.start_x, self.start_y, self.radius)
            self.all_particles.append(particle)

        # Create an empty list to store the positions (x and y) of the pixels forming the growing crystal
        self.crystal_position = []

        # Initialise min and max x, y to define a rectangular crystal domain (limits of crystal)
        self.min_x, self.min_y = self.start_x, self.start_y
        self.max_x, self.max_y = self.start_x, self.start_y


    def on_init(self):
        pygame.init()
        pygame.display.set_caption("2D Diffusion Limited Aggregation")      # Window title

        self.displaySurface = pygame.display.set_mode(self.size)      # Create display surface
        self.pixelArray = pygame.PixelArray(self.displaySurface)      # Create pixel array

        self.isRunning = True

        self.start_time = pygame.time.get_ticks()       # Set a timer
    

    def on_event(self, event):
        '''
        Called during main on_execute() loop which loops over all events continuously during the simulation.
        '''
        ### In the event we want to quit the game
        if event.type == pygame.QUIT:
            time = pygame.time.get_ticks() - self.start_time
            print("A total of", time/1000, "seconds have elapsed.")
            self.isRunning = False


    def gen_seed(self, particle, seed_shape):
        '''
        Create seed - must be same colour as other particles or they won't stick!
        '''
        if seed_shape == 'dot':
            self.pixelArray[self.start_x, self.start_y] = self.crystalColor

        elif seed_shape == 'line':
            pygame.draw.line(self.displaySurface, self.crystalColor, (self.start_x-50, self.start_y), (self.start_x+50, self.start_y))

        elif seed_shape == 'circle':
            pygame.draw.circle(self.displaySurface, self.crystalColor, (self.start_x, self.start_y), 30, width=1)

        elif seed_shape == 'ellipse':
            pygame.draw.ellipse(self.displaySurface, self.crystalColor, ((self.start_x, self.start_y), (32, 20)), width = 1)

        elif seed_shape == 'square':
            pygame.draw.rect(self.displaySurface, self.crystalColor, ((self.start_x, self.start_y), (50, 50)), width = 1)

        elif seed_shape == 'star':   # because my dad asked me to!
            x = self.start_x
            y = self.start_y
            star_points  = [(x, y-76), (x+20, y-25), (x+73, y-28), (x+28, y+5), (x+42, y+55), (x, y+23), (x-42, y+55), (x-28, y+5), (x-73, y-28), (x-20, y-25)]
            pygame.draw.polygon(self.displaySurface, self.crystalColor, star_points)


    def on_loop(self):
        '''
        Adds one pixel to each random walk
        '''
        ss = 1    # set step size
        # print(self.min_x, self.min_y, self.max_x, self.max_y)
        for particle in self.all_particles:
            # (dx, dy) = random.choice([(0, ss), (0, -ss), (ss, 0), (-ss, 0)])
            (dx, dy) = random.choice([(0, ss), (0, -ss), (ss, 0), (-ss, 0), (ss, -ss), (-ss, ss), (ss, ss), (-ss, -ss)])

            ### Assign to new x and y variables to keep a record of current and future position
            new_x = particle.x + dx
            new_y = particle.y + dy

            ### Call wrap_around method to wrap around movement around based on a chosen domain shape
            new_x, new_y = self.wrap_around(self.domain_shape, new_x, new_y)

            ### Call the generate seed method based on a chosen seed shape
            self.gen_seed(particle, self.seed_shape)

            ### Recolour existing (and growing) crystal each loop iteration
            # for coordinate in self.crystal_position:
            #     self.pixelArray[coordinate[0], coordinate[1]] = self.crystalColor

            ### Check if pixel has already been covered by walker 
            if self.pixelArray[new_x, new_y] == self.crystalColor:  # light gray
                self.updateFlag = True

                # Modify simulation domain as crystal grows
                if particle.x < self.min_x:
                    self.min_x = particle.x
                if particle.x > self.max_x:
                    self.max_x = particle.x
                if particle.y < self.min_y:
                    self.min_y = particle.y
                if particle.y > self.max_y:
                    self.max_y = particle.y
                
                self.restrict_domain(self.domain_shape)

            else:
                self.updateFlag = False
                particle.x, particle.y = new_x, new_y

            self.on_render(particle)    # call on_render here to be able to pass in particle attributes x, y

        pygame.display.update()
        
        # if self.all_particles:
        #     self.displaySurface.fill((0,0,0,))      # Removes previous path of particles


    def wrap_around(self, domain_shape, new_x, new_y):
        '''
        Wrap-around: ensure random walk does not disappear off square screen, otherwise application quits
        '''
        if domain_shape == 'square':
            if new_x < self.sqdomainMin_x:
                new_x = self.sqdomainMax_x
            if new_x > self.sqdomainMax_x:
                new_x = self.sqdomainMin_x
            if new_y < self.sqdomainMin_y:
                new_y = self.sqdomainMax_y
            if new_y > self.sqdomainMax_y:
                new_y = self.sqdomainMin_y
    
        elif domain_shape == 'circle':
            sqx = (new_x - self.start_x)**2
            sqy = (new_y - self.start_y)**2
            r = math.sqrt(sqx + sqy)
            if r > self.radius:
                new_x = self.start_x / self.radius * r
                new_y = self.start_y / self.radius * r
                # new_x = self.start_x - (new_x - self.start_x)
                # new_y = self.start_y - (new_y - self.start_y)
        
        # print(round(r), new_x, new_y)
        return new_x, new_y

    def restrict_domain(self, domain_shape):
        '''
        Ensure domain minima and maxima never extend beyond the screen boundaries
        '''
        if domain_shape == 'square':
            self.sqdomainMin_x = max([self.min_x - self.padSize, 1])
            self.sqdomainMax_x = min([self.max_x + self.padSize, self.width - 1])
            self.sqdomainMin_y = max([self.min_y - self.padSize, 1])
            self.sqdomainMax_y = min([self.max_y + self.padSize, self.width - 1])

        elif domain_shape == 'circle':
            pass
            

    def on_render(self, particle):
        '''
        Updates the pixel array if a particle is allocated to the growing crystal, otherwise shows movement of particle on their random walks
        '''

        ### If particle sticks, append its coordinates to list and particle.stick = True stops it from moving any further
        if self.updateFlag:  

            ### Freeze animation if crystal grows to a specified size
            x = particle.x - self.start_x
            y = particle.y - self.start_y
            distance = math.sqrt(x**2 + y**2)
            if distance > self.crystal_size_limit:
                pygame.time.wait(1000000)

            self.crystal_position.append((particle.x, particle.y))
            self.pixelArray[particle.x, particle.y] = self.crystalColor

            ### Remove particle from all_particles list OR respawn from domain square
            # self.all_particles.remove(particle)
            ### Recycle the particle once it's stuck
            particle.spawn_shape(self.sqdomainMin_x, self.sqdomainMax_x, self.sqdomainMin_y, self.sqdomainMax_y, self.start_x, self.start_y, self.radius)


        ### Show individual particles moving
        # if not self.updateFlag: 
        #     self.pixelArray[particle.x, particle.y] = 0x00FF00   # green



    def on_execute(self):
        '''
        Method called when application is first run
        '''
        ### Makes sure application stops is on_init() is False
        if self.on_init() == False:
            self.isRunning = False

        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            # self.on_render()   # moved to end of on_loop to carry over particle attributes

        pygame.quit()


if __name__ == '__main__':
    test = Application(300)
    test.on_execute()