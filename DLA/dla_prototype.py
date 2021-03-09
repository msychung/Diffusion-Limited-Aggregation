import random
import numpy as np
import pygame


class Application():

    def __init__(self):
        # Initialise display surface, set its size and initialise pixel array and colour
        self.displaySurface = None
        self.size = self.width, self.height = 962, 601      # size of display screen
        self.pixelArray = None
        self.pixelColor = None
        
        # Set starting co-ordinates
        self.start_x = round(self.width/2)
        self.start_y = round(self.height/2)  

        # Create x and y variables to store co-ordinates
        self.x = self.start_x
        self.y = self.start_y 

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("2D Diffusion Limited Aggregation")

        self.displaySurface = pygame.display.set_mode(self.size)      # Create display surface
        self.pixelArray = pygame.PixelArray(self.displaySurface)      # Create pixel array
        self.pixelColor = (220, 220, 220)                             # Set pixel colour in RGB
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
        (dx, dy) = random.choice([(0, ss), (0, -ss), (ss, 0), (-ss, 0)])

        ### Assign to new x and y variables to keep a record of current and future position
        self.x += dx
        self.y += dy

        ### Ensure random walk does not disappear off screen, otherwise application quits
        if self.x < 0:
            self.x = 0
        if self.x > (self.width - 1):
            self.x = self.width - 1
        if self.y < 0:
            self.y = 0
        if self.y > (self.height - 1):
            self.y = self.height - 1

        ### Check if pixel has already been covered by walker (need to use hex colour codes)
        if self.pixelArray[self.x, self.y] == 0xDCDCDC:  # light gray
            self.pixelColor = (225, 0, 0)

        elif self.pixelArray[self.x, self.y] == 0xFF0000:  # red
            self.pixelColor = (255, 0, 0)

        else:
            self.pixelColor = (220, 220, 220)

    def on_render(self):
        '''
        Updates the pixel array IF a particle is allocated to the growing crystal
        '''
        self.pixelArray[self.x, self.y] = self.pixelColor

        # Update the display
        pygame.display.update()

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
    test = Application()
    test.on_execute()