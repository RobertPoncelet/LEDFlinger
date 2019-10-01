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

import collections, math


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
            if self.has_finished():
                return
            d = ImageDraw.Draw(self.buffer)
            d.ellipse([self.pos[0]-4, self.pos[1]-4, self.pos[0]+4, self.pos[1]+4], fill=self.colour)
        else:
            self.buffer.fill(BLACK)
            pygame.draw.circle(self.buffer, self.colour, self.pos, 4)
        if self.pos == self.start:
            self.update_pos()


class TextAnimation(Animation):
    def __init__(self, buffer, input_text):
        super().__init__(buffer)
        self.drawn = False
        self.angle = 0
        self.text = Image.new("RGB", size, BLACK) # TODO: minimum necessary size
        font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 10)
        draw = ImageDraw.Draw(self.text)
        draw.text((0, 0), input_text, font=font, fill=WHITE)

    def should_update(self):
        return self.angle < self.buffer.size[1] #not self.drawn

    def has_finished(self):
        return not self.should_update()

    def update(self):
        self.buffer.paste(BLACK, [0, 0, self.buffer.size[0], self.buffer.size[1]])
        self.angle += 1
        self.buffer.paste(self.text.resize((self.buffer.size[0], self.angle)), [0, 0])


class BackgroundAnimation(Animation):
    def __init__(self, buffer, colour):
        super().__init__(buffer)
        self.colour = colour
        self.drawn = False

    def should_update(self):
        return not self.drawn

    def has_finished(self):
        return self.drawn

    def update(self):
        self.buffer.paste(self.colour, [0, 0, self.buffer.size[0], self.buffer.size[1]])
        self.drawn = True


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
            im = Image.new("RGB", size, BLACK)
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

