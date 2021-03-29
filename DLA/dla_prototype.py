import random
import math
import numpy as np
import pygame

class Particle():

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def update(self, x, y):
        self.x = x
        self.y = y


class Application():

    def __init__(self, n, seed_shape, spawn_shape, padSize, radius, crystal_size_limit, view=False):
        # Initialise display surface, set its size and initialise pixel array and colour
        self.size = self.width, self.height = 800, 600      # size of display screen
        self.crystalColor = 0xDCDCDC        # grey
        self.n = n
        
        # Set seed, spawn and domain shapes
        self.seed_shape = seed_shape
        self.spawn_shape = spawn_shape

        # Set centre co-ordinates
        self.start_x = round(self.width/2)
        self.start_y = round(self.height/2)  
        self.padSize = padSize
        
        # Define a square domain that is padSize pixels larger than crystal domain
        self.sqdomainMin_x = self.start_x - self.padSize
        self.sqdomainMax_x = self.start_x + self.padSize
        self.sqdomainMin_y = self.start_y - self.padSize
        self.sqdomainMax_y = self.start_y + self.padSize

        # Define circle domain radius in pixels
        self.radius = padSize

        # Set a size limit for the growing crystal
        self.crystal_size_limit = crystal_size_limit

        # Set a stickiness coefficient
        self.stick_coeff = 0.8

        # Use composition to create n particle instances using the Particle class
        
        self.all_particles = []

        for i in range(n):
            if self.spawn_shape == 'square':
                particle = Particle(*self.square_spawn())

            elif self.spawn_shape == 'circle':
                particle = Particle(*self.circle_spawn())

            self.all_particles.append(particle)

        # Create an empty list to store the positions (x and y) of the pixels forming the growing crystal
        self.crystal_position = []

        # Initialise min and max x, y to define a rectangular crystal domain (limits of crystal)
        self.min_x, self.min_y = self.start_x, self.start_y
        self.max_x, self.max_y = self.start_x, self.start_y

        self.on_execute()


    def on_init(self):
        pygame.init()
        pygame.display.set_caption("2D Diffusion Limited Aggregation")      # Window title

        self.displaySurface = pygame.display.set_mode(self.size)      # Create display surface
        self.pixelArray = pygame.PixelArray(self.displaySurface)      # Create pixel array
        self.gen_seed()
        self.isRunning = True
        self.start_time = pygame.time.get_ticks()       # Set a timer

        # if self.view == False:
        #     pygame.display.quit()
    

    def on_event(self, event):
        '''
        Called during main on_execute() loop which loops over all events continuously during the simulation.
        '''
        ### In the event we want to quit the game
        if event.type == pygame.QUIT:
            time = pygame.time.get_ticks() - self.start_time
            print("A total of", time/1000, "seconds has elapsed.")
            self.isRunning = False


    def gen_seed(self):
        '''
        Create seed - must be same colour as other particles or they won't stick!
        '''
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
        # Randomly choose a position on a side of a square for a particle to spawn along
        newSide = random.choice([1, 2, 3, 4])
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
        # Randomly choose a position on a circle of radius r for the particle to spawn on
        theta = random.random() * 2 * math.pi

        x = int(self.start_x + math.cos(theta)*self.radius)
        y = int(self.start_y + math.sin(theta)*self.radius)

        return x, y


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
            new_x, new_y = self.wrap_around(particle, new_x, new_y)

            ### Call the generate seed method based on a chosen seed shape

            ### Recolour existing (and growing) crystal each loop iteration
            # for coordinate in self.crystal_position:
            #     self.pixelArray[coordinate[0], coordinate[1]] = self.crystalColor

            ### Check if pixel has already been covered by walker 
            if self.pixelArray[new_x, new_y] == self.crystalColor and random.random() <= self.stick_coeff:  # light gray
                self.pixelArray[particle.x, particle.y] = self.crystalColor
                self.crystal_position.append((particle.x, particle.y))

                x = particle.x - self.start_x
                y = particle.y - self.start_y
                distance = math.sqrt(x**2 + y**2)

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

                ### Remove particle from all_particles list OR respawn from domain square
                # self.all_particles.remove(particle)
                ### Recycle the particle once it's stuck
                if self.spawn_shape == 'square':
                    particle.update(*self.square_spawn())
                
                elif self.spawn_shape == 'circle':
                    particle.update(*self.circle_spawn())

            else:
                particle.x, particle.y = new_x, new_y
                
        pygame.display.update()
        
        # if self.all_particles:
        #     self.displaySurface.fill((0,0,0,))      # Removes previous path of particles


    def wrap_around(self, particle, new_x, new_y):
        '''
        Wrap-around: ensure random walk does not disappear off square screen, otherwise application quits
        '''
        if self.spawn_shape == 'square':
            if new_x < self.sqdomainMin_x:
                new_x = self.sqdomainMax_x
            if new_x > self.sqdomainMax_x:
                new_x = self.sqdomainMin_x
            if new_y < self.sqdomainMin_y:
                new_y = self.sqdomainMax_y
            if new_y > self.sqdomainMax_y:
                new_y = self.sqdomainMin_y
    
        elif self.spawn_shape == 'circle':
            sqx = (new_x - self.start_x)**2
            sqy = (new_y - self.start_y)**2
            r = math.sqrt(sqx + sqy)
            
            if r > self.radius:
                new_x = -particle.x
                new_y = -particle.y
        
        return new_x, new_y


    def restrict_domain(self):
        '''
        Ensure domain minima and maxima never extend beyond the screen boundaries
        '''
        if self.spawn_shape == 'square':
            self.sqdomainMin_x = max([self.min_x - self.padSize, 1])
            self.sqdomainMax_x = min([self.max_x + self.padSize, self.width - 1])
            self.sqdomainMin_y = max([self.min_y - self.padSize, 1])
            self.sqdomainMax_y = min([self.max_y + self.padSize, self.width - 1])

        elif self.spawn_shape == 'circle':
            max_radius = 0

            for pixel in self.crystal_position:
                x = pixel[0] - self.start_x
                y = pixel[1] - self.start_y
                radius = np.sqrt(x**2 + y**2)

                if radius > max_radius:
                    max_radius = radius

            self.radius = max_radius + self.padSize
            
        ### Show individual particles moving
        if not self.updateFlag: 
            self.pixelArray[particle.x, particle.y] = 0x00FF00   # green


    def on_execute(self):
        '''
        Method called when application is first run
        '''
        ### Makes sure application stops is on_init() is False
        self.on_init()
      
        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            # self.on_render()   # moved to end of on_loop to carry over particle attributes

        pygame.quit()


# Prevents these conditions applying when running the file externally (i.e. from frac_dim.py)
if __name__ == '__main__':
    test = Application(1000, 'dot', 'circle', 50, 40, 100)