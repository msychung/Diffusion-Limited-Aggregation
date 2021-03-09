import random
import numpy as np
import pygame

class Particle():

    def __init__(self, width, height):
        # Set starting co-ordinates
        self.x = round(width/2)
        self.y = round(height/2) 

        self.stick= False 


class Application():

    def __init__(self, n):
        # Initialise display surface, set its size and initialise pixel array and colour
        self.displaySurface = None
        self.size = self.width, self.height = 962, 601      # size of display screen
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
        
        self.padSize = 30
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
        ss = 2    # set step size

        for particle in self.all_particles:
            if particle.stick:
                continue

            # (dx, dy) = random.choice([(0, ss), (0, -ss), (ss, 0), (-ss, 0)])
            (dx, dy) = random.choice([(0, ss), (0, -ss), (ss, 0), (-ss, 0), (ss, -ss), (-ss, ss), (ss, ss), (-ss,-ss)])

            ### Assign to new x and y variables to keep a record of current and future position
            new_x = particle.x + dx
            new_y = particle.y + dy

            ### Ensure random walk does not disappear off screen, otherwise application quits
            if new_x < 0:
                new_x = 0
            if new_x > (self.width - 1):
                new_x = self.width - 1
            if new_y < 0:
                new_y = 0
            if new_y > (self.height - 1):
                new_y = self.height - 1

            ### Check if pixel has already been covered by walker (need to use hex colour codes)
            if self.pixelArray[new_x, new_y] == self.crystalColor:  # light gray
                self.updateFlag = True

            else:
                self.updateFlag = False
                particle.x, particle.y = new_x, new_y

            self.on_render(particle)    # call on_render here to be able to pass in particle attributes x, y

        pygame.display.update()
        self.displaySurface.fill((0,0,0,))      # Removes previous path of particles


    def on_render(self, particle):
        '''
        Updates the pixel array if a particle is allocated to the growing crystal, otherwise shows movements of particles on their random walks
        '''
        ## Create seed - must be same colour as other particles or they won't stick!
        self.pixelArray[self.start_x - 100, self.start_y - 100] = self.crystalColor

        ### Recolour crystal each time
        for coordinate in self.crystal_position:
            self.pixelArray[coordinate[0], coordinate[1]] = self.crystalColor

        ### If particle sticks, set its pixel to grey and particle.stick = True stops it from moving any further
        if self.updateFlag:  
            self.crystal_position.append((particle.x, particle.y))

            # Reset update flag and x, y co-ordinates to restart random walk
            self.updateFlag = False
            particle.stick = True

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
    test = Application(500)
    test.on_execute()