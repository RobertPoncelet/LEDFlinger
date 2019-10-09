from sys import platform
linux = platform == "linux"

if linux:
    from PIL import Image, ImageFont, ImageDraw, ImageChops
else:
    import pygame

from colours import BLACK, WHITE

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
        self.angle = 0
        if linux:
            self.text = Image.new("1", (32, 8), BLACK) # TODO: minimum necessary size
            font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 12)
            draw = ImageDraw.Draw(self.text)
            draw.text((-2, -2), input_text, font=font, fill=WHITE)
        else:
            pass # TODO

    def should_update(self):
        return self.angle < (self.buffer.size[1] if linux else self.buffer.get_size()[1])

    def has_finished(self):
        return not self.should_update()

    def update(self):
        self.angle += 1
        if linux:
            self.buffer.paste(BLACK, [0, 0, self.buffer.size[0], self.buffer.size[1]])
            self.buffer.paste(self.text.resize((self.buffer.size[0], self.angle)), [0, 0])
        else:
            pass # TODO


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
        if linux:
            self.buffer.paste(self.colour, [0, 0, self.buffer.size[0], self.buffer.size[1]])
        else:
            pass # TODO
        self.drawn = True
