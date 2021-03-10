import random
import numpy as np
import pygame

class Particle():

    def __init__(self, width, height):
        # Set starting co-ordinates
        self.x = round(width/2)
        self.y = round(height/2) 


class Application():

    def __init__(self, n):
        # Initialise display surface, set its size and initialise pixel array and colour
        self.displaySurface = None
        self.size = self.width, self.height = 640, 360      # size of display screen
        self.pixelArray = None
        self.crystalColor = 0xDCDCDC
        
        # Set starting co-ordinates
        self.start_x = round(self.width/2)
        self.start_y = round(self.height/2)  

        self.updateFlag = False

        self.all_particles = []
        for i in range(n):
            particle = Particle(self.width, self.height)   #  yaaayy composition! 
            self.all_particles.append(particle)

        self.crystal_position = []
        
        # Initialise min and max x, y to define a rectangular crystal domain (limits of crystal)
        self.min_x, self.min_y = particle.x, particle.y
        self.max_x, self.max_y = particle.x, particle.y
        self.padSize = 50

        # Define a domain that is padSize pixels larger than crystal domain
        self.domainMin_x = self.start_x - self.padSize
        self.domainMax_x = self.start_x + self.padSize
        self.domainMin_y = self.start_y - self.padSize
        self.domainMax_y = self.start_y + self.padSize


    def on_init(self):
        pygame.init()
        pygame.display.set_caption("2D Diffusion Limited Aggregation")

        self.displaySurface = pygame.display.set_mode(self.size)      # Create display surface
        self.pixelArray = pygame.PixelArray(self.displaySurface)      # Create pixel array

        self.isRunning = True
    

    def on_event(self, event):
        '''
        Called during main on_execute() loop which loops over all events continuously during the simulation.
        '''
        ### In the event we want to quit the game
        if event.type == pygame.QUIT:
            self.isRunning = False


    def on_loop(self):
        '''
        Adds one pixel to each random walk
        '''
        ss = 1    # set step size

        for particle in self.all_particles:
            # (dx, dy) = random.choice([(0, ss), (0, -ss), (ss, 0), (-ss, 0)])
            (dx, dy) = random.choice([(0, ss), (0, -ss), (ss, 0), (-ss, 0), (ss, -ss), (-ss, ss), (ss, ss), (-ss,-ss)])

            ### Assign to new x and y variables to keep a record of current and future position
            new_x = particle.x + dx
            new_y = particle.y + dy

            ### Wrap-around: ensure random walk does not disappear off screen, otherwise application quits
            if new_x < self.domainMin_x:
                new_x = self.domainMax_x
            if new_x > self.domainMax_x:
                new_x = self.domainMin_x
            if new_y < self.domainMin_y:
                new_y = self.domainMax_y
            if new_y > self.domainMax_y:
                new_y = self.domainMin_y

            ### Create seed - must be same colour as other particles or they won't stick!
            self.pixelArray[self.start_x - 30, self.start_y - 30] = self.crystalColor

            ### Recolour crystal each time
            for coordinate in self.crystal_position:
                self.pixelArray[coordinate[0], coordinate[1]] = self.crystalColor

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
                    
                # Ensure domain minima and maxima never less/more than 1
                self.domainMin_x = max([self.min_x - self.padSize, 1])
                self.domainMax_x = min([self.max_x + self.padSize, self.width - 1])
                self.domainMin_y = max([self.min_y - self.padSize, 1])
                self.domainMax_y = min([self.max_y + self.padSize, self.width - 1])

            else:
                self.updateFlag = False
                particle.x, particle.y = new_x, new_y

            self.on_render(particle)    # call on_render here to be able to pass in particle attributes x, y

        pygame.display.update()
        if self.all_particles:   # List evaluates to False if empty
            self.displaySurface.fill((0,0,0,))      # Removes previous path of particles


    def on_render(self, particle):
        '''
        Updates the pixel array if a particle is allocated to the growing crystal, otherwise shows movements of particles on their random walks
        '''
        ### If particle sticks, set its pixel to grey and particle.stick = True stops it from moving any further
        if self.updateFlag:  
            self.crystal_position.append((particle.x, particle.y))

            # Reset update flag and x, y co-ordinates to restart random walk
            # self.updateFlag = False
            self.all_particles.remove(particle)

        if not self.updateFlag:
            self.pixelArray[particle.x, particle.y] = 0x00FF00   # green


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
            # self.on_render()

        pygame.quit()


if __name__ == '__main__':
    test = Application(5)
    test.on_execute()
