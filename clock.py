import animation
import datetime

class ClockAnimation(Animation):
    def __init__(self, buffer):
        super().__init__(buffer)
        self.drawn = False
        now = datetime.datetime.now().time()
        self.time = str(now.hour) + str(now.minute)
        self.sheet = Image.open("sheet.png")

    def should_update(self):
        return not self.drawn

    def has_finished(self):
        return self.drawn

    def update(self):
        for d in enumerate(self.time):
            i = d[0]
            digit = int(d[1])
            srcbox = [8*digit, 4*8, 8*digit+8, 4*8+8]
            dstbox = [8*i, 0]
            self.buffer.paste(self.sheet.crop(srcbox), dstbox)
            #self.buffer.convert("1")
        self.drawn = True
