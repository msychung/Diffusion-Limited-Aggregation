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
        self.size = self.width, self.height = 962, 601      # size of display screen
        self.pixelArray = None
        self.pixelColor = None
        
        # Set starting co-ordinates
        self.start_x = round(self.width/2)
        self.start_y = round(self.height/2)  

        # # Create x and y variables to store co-ordinates
        # self.x = self.start_x
        # self.y = self.start_y 

        self.updateFlag = False

        self.particle = Particle(self.width, self.height)
        

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("2D Diffusion Limited Aggregation")

        self.displaySurface = pygame.display.set_mode(self.size)      # Create display surface
        self.pixelArray = pygame.PixelArray(self.displaySurface)      # Create pixel array
        self.pixelColor = (220, 220, 220)                             # Set pixel colour in RGB
        self.isRunning = True

        ### Create a seed point
        # self.pixelArray[self.start_x - 50, self.start_y - 50] = 0xDCDCDC    # Must be same colour as other particles otherwise they won't stick!
        # pygame.display.update()
    
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
        (dx, dy) = random.choice([(0, ss), (0, -ss), (ss, 0), (-ss, 0)])

        ### Assign to new x and y variables to keep a record of current and future position
        new_x = self.particle.x + dx
        new_y = self.particle.y + dy

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
        if self.pixelArray[new_x, new_y] == 0xDCDCDC:  # light gray
            self.updateFlag = True

        else:
            self.updateFlag = False
            self.particle.x, self.particle.y = new_x, new_y

    def on_render(self):
        '''
        Updates the pixel array IF a particle is allocated to the growing crystal
        '''
        self.displaySurface.fill((0,0,0,))

        ### Create seed
        self.pixelArray[self.start_x - 50, self.start_y - 50] = 0xDCDCDC    # Must be same colour as other particles otherwise they won't stick!
        pygame.display.update()

        if self.updateFlag:  
            self.pixelArray[self.particle.x, self.particle.y] = 0xDCDCDC

            # Update the display
            pygame.display.update()

            # Reset update flag and x, y co-ordinates to restart random walk
            self.updateFlag = False
            self.particle.x, self.particle.y = self.start_x, self.start_y

        if not self.updateFlag:
            self.pixelArray[self.particle.x, self.particle.y] = 0x00FF00
            pygame.display.update()

        # self.pixelArray[self.x, self.y] = self.pixelColor
        # pygame.display.update()

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
            self.on_render()

        pygame.quit()

if __name__ == '__main__':
    test = Application(5)
    test.on_execute()