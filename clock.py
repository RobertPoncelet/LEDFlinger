from animation import Animation
from PIL import Image, ImageChops
import datetime

class ClockAnimation(Animation):
    def __init__(self, buffer):
        super().__init__(buffer)
        self.oldtime = "0000"
        self.refresh_time()
        self.step = 0
        self.sheet = Image.open("sheet.png")

    def refresh_time(self):
        now = datetime.datetime.now().time()
        hour = str(now.minute).zfill(2) # TODO: change back
        minute = str(now.second).zfill(2)
        self.time = hour + minute

    def sheet_box(self, digit, step, movein):
        if not movein:
            step += 5
        return (digit*8, step*8, digit*8+8, step*8+8)

    def should_update(self):
        self.refresh_time()
        return self.time != self.oldtime

    def has_finished(self):
        return False

    def update(self):
        for d in enumerate(self.time):
            i = d[0]
            if self.oldtime[i] == d[1]:
                continue
            digit = int(d[1])
            insrcbox = self.sheet_box(digit, self.step, True)
            inim = self.sheet.crop(insrcbox).convert("L")
            dstbox = (8*i, 0)
            if self.step < 5:
                outdigit = int(self.oldtime[i])
                outsrcbox = list(self.sheet_box(outdigit, self.step, False))
                outim = self.sheet.crop(outsrcbox).convert("L")
                inim = ImageChops.add(inim, outim)
            self.buffer.paste(inim, dstbox)
        self.step += 1
        if self.step >= 5:
            self.oldtime = self.time
            self.step = 0
