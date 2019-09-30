from sys import platform
linux = platform == "linux"

if linux:
    from luma.led_matrix.device import max7219
    from luma.core.interface.serial import spi, noop
    from luma.core.render import canvas
    from luma.core.legacy import text
    from luma.core.legacy.font import proportional, LCD_FONT

    from PIL import Image, ImageDraw, ImageChops

    import time
else:
    import pygame

import collections
#from math import pi


class Animation(object):
    def __init__(self, buffer):
        self.buffer = buffer


class CircleAnimation(Animation):
    def __init__(self, buffer, colour, start, end, waiting_for=None):
        super().__init__(buffer)
        self.pos = list(start)
        self.colour = colour
        self.start = list(start)
        self.end = list(end)
        self.waiting_for = waiting_for

    def should_update(self):
        if self.waiting_for is None:
            return True
        return self.waiting_for.has_finished()

    def has_finished(self):
        return self.pos == self.end

    def update_pos(self):
        for i in range(2):
            if self.pos[i] < self.end[i]:
                self.pos[i] += 1
            elif self.pos[i] > self.end[i]:
                self.pos[i] -= 1

    def update(self):
        if self.pos != self.start:
            self.update_pos()
        if linux:
            self.buffer.paste(BLACK, [0, 0, self.buffer.size[0], self.buffer.size[1]])
            d = ImageDraw.Draw(self.buffer)
            d.ellipse([self.pos[0]-2, self.pos[1]-2, self.pos[1]+2, self.pos[1]+2], outline=self.colour)
        else:
            self.buffer.fill(BLACK)
            pygame.draw.circle(self.buffer, self.colour, self.pos, 4)
        if self.pos == self.start:
            self.update_pos()


class Layer(object):
    def __init__(self, size, flags=0):
        if linux:
            self.buffer = Image.new("RGB", size, BLACK)
        else:
            self.buffer = pygame.Surface(size)
        self.flags = flags
        self.queue = collections.deque()

    def add_animation(self, anim):
        anim.buffer = self.buffer
        self.queue.append(anim)

    def should_update(self):
        return len(self.queue) > 0 and self.queue[0].should_update()

    def update(self):
        if not self.should_update():
            return
        self.queue[0].update()
        if self.queue[0].has_finished():
            self.queue.popleft()


# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Set the height and width of the screen

scaling_factor = 16
screen_width, screen_height = 32, 8

if linux:
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    # TODO: args
    device = max7219(serial, width=screen_width, height=screen_height) #, rotate=rotate, block_orientation=block_orientation)
else:
    # Initialize the game engine
    pygame.init()
    win = pygame.display.set_mode((screen_width*scaling_factor, screen_height*scaling_factor))
    pygame.display.set_caption("Example code for the draw module")


size = (screen_width, screen_height)
layers = [Layer(size), Layer(size)] #TODO: , flags=pygame.BLEND_ADD)]
first_anim = CircleAnimation(None, BLUE, (0, 0), (screen_width, screen_height))
layers[0].add_animation(first_anim)
layers[0].add_animation(CircleAnimation(None, GREEN, (0, screen_height), (screen_width, 0)))
layers[1].add_animation(CircleAnimation(None, RED, (screen_width, 0), (0, screen_height), waiting_for=first_anim))

#Loop until the user clicks the close button.
done = False
if not linux:
    clock = pygame.time.Clock()

try:
    while not done:

        if linux:
            time.sleep(1./30.)
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

        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        if linux:
            im = Image.new("RGB", size, BLACK)
        for layer in layers:
            if linux:
                im = ImageChops.add(im, layer.buffer)
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

