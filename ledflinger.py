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
import math

# Set the height and width of the screen

scaling_factor = 16
screen_width, screen_height = 32, 8

if linux:
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    # TODO: args
    device = max7219(serial, width=screen_width, height=screen_height, block_orientation=90, cascaded=4, blocks_arranged_in_reverse_order=True)
else:
    # Initialize the game engine
    pygame.init()
    win = pygame.display.set_mode((screen_width*scaling_factor, screen_height*scaling_factor))
    pygame.display.set_caption("Example code for the draw module")


size = (screen_width, screen_height)
if linux:
    flaggy = 0
else:
    flaggy = pygame.BLEND_ADD
layers = [Layer(size), Layer(size, flags=flaggy), Layer(size, flags=flaggy), Layer(size, flags=flaggy)]
text_anim = TextAnimation(None, "Hello")
first_anim = CircleAnimation(None, WHITE, (0, 0), (screen_width, screen_height), waiting_for=text_anim)
layers[0].add_animation(first_anim)
layers[0].add_animation(CircleAnimation(None, WHITE, (0, screen_height), (screen_width, 0), waiting_for=text_anim))
layers[1].add_animation(CircleAnimation(None, WHITE, (screen_width, 0), (0, screen_height), waiting_for=first_anim))
layers[2].add_animation(text_anim)
layers[3].add_animation(BackgroundAnimation(None, WHITE))

#Loop until the user clicks the close button.
done = False
if not linux:
    clock = pygame.time.Clock()

try:
    while not done:

        if linux:
            time.sleep(1./30.) # TODO: replace with luma.core.sprite_system.framerate_regulator
        else:
            # This limits the while loop to a max of 30 times per second.
            # Leave this out and we will use all CPU we can.
            clock.tick(30)

        if not linux:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop

        # START COMPOSITION
        update = False
        for layer in layers:
            if layer.should_update():
                update = True
                break
        if not update:
            continue

        for layer in layers:
            layer.update()

        if linux:
            im = Image.new("1", size, BLACK)
        for layer in layers:
            if linux:
                im = ImageChops.difference(im, layer.buffer)
            else:
                win.blit(pygame.transform.scale(layer.buffer, win.get_rect().size), (0, 0), special_flags=layer.flags)

        if linux:
            device.display(im.convert("1"))
        else:
            pygame.display.flip()
        # END COMPOSITION

except KeyboardInterrupt:
    if not linux:
        # Be IDLE friendly
        pygame.quit()

if not linux:
    pygame.quit()

