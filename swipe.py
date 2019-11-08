from animation import Animation
from PIL import Image #, ImageDraw
from colours import BLACK, WHITE

class SwipeAnimation(Animation):
    def __init__(self, buffer, move_in, update_rate=15, step_size=2):
        super().__init__(buffer, update_rate)
        self.move_in = move_in
        self.step = 0
        self.step_size = step_size
        self.buffer.paste(BLACK if move_in else WHITE, (0, 0, self.buffer.width, self.buffer.height))

    def should_update(self):
        return self.step < self.buffer.width + self.buffer.height

    def has_finished(self):
        return not self.should_update()

    def update(self):
        colour = WHITE if self.move_in else BLACK
        #if self.step > self.height:
        #    self.buffer.paste(colour, (0, 0, self.buffer.step - self.buffer.height, self.buffer.height))#
        for y in range(min(self.step+1, self.buffer.height)):
            for bit in range(self.step_size):
                x = self.step - y - bit
                if x >= 0 and x < self.buffer.width:
                    self.buffer.putpixel((x, y), colour)
        self.step += self.step_size
