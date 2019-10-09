from sys import platform
linux = platform == "linux"

if linux:
    from luma.led_matrix.device import max7219
    from luma.core.interface.serial import spi, noop
    from luma.core.render import canvas
    from luma.core.legacy import text
    from luma.core.legacy.font import proportional, LCD_FONT, CP437_FONT

    from PIL import Image, ImageFont, ImageDraw, ImageChops

    import time
else:
    import pygame

from layer import Layer
from animation import *
from colours import BLACK, WHITE

class Compositor(object):
    def __init__(self, size):
        self.scaling_factor = 16
        self.size = size
        self.screen_width, self.screen_height = self.size
        self.layers = []
        self.done = False

        if linux:
            # create matrix device
            self.serial = spi(port=0, device=0, gpio=noop())
            # TODO: args
            self.device = max7219(self.serial, width=self.screen_width, height=self.screen_height,
                             block_orientation=90, cascaded=4, blocks_arranged_in_reverse_order=True)
        else:
            # Initialize the game engine
            pygame.init()
            self.win = pygame.display.set_mode((self.screen_width*self.scaling_factor, self.screen_height*self.scaling_factor))
            pygame.display.set_caption("Example code for the draw module")


    def run(self):
        #Loop until the user clicks the close button.
        if not linux:
            clock = pygame.time.Clock()

        try:
            while not self.done:

                if linux:
                    time.sleep(1./30.) # TODO: replace with luma.core.sprite_system.framerate_regulator
                else:
                    # This limits the while loop to a max of 30 times per second.
                    # Leave this out and we will use all CPU we can.
                    clock.tick(30)

                if not linux:
                    for event in pygame.event.get(): # User did something
                        if event.type == pygame.QUIT: # If user clicked close
                            self.done=True # Flag that we are done so we exit this loop

                # START COMPOSITION
                update = False
                for layer in self.layers:
                    if layer.should_update():
                        update = True
                        break
                if not update:
                    continue

                for layer in self.layers:
                    layer.update()

                if linux:
                    im = Image.new("1", self.size, BLACK)
                for layer in self.layers:
                    if linux:
                        im = ImageChops.difference(im, layer.buffer)
                    else:
                        self.win.blit(pygame.transform.scale(layer.buffer, self.win.get_rect().size), (0, 0), special_flags=layer.flags)

                if linux:
                    self.device.display(im)
                else:
                    pygame.display.flip()
                # END COMPOSITION

        except KeyboardInterrupt:
            if not linux:
                # Be IDLE friendly
                pygame.quit()

        if not linux:
            pygame.quit()

