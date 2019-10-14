from animation import Animation
from PIL import Image, ImageChops
from colours import BLACK, WHITE
import datetime

class ClockAnimation(Animation):
    def __init__(self, buffer):
        super().__init__(buffer)
        self.oldtime = "9999"
        self.refresh_time()
        self.step = 0
        self.show_colon = False
        self.old_show_colon = False
        self.sheet = Image.open("sheet.png")
        # TODO: make sure animations are initialised with a proper buffer, then uncomment the next line
        #self.buffer.paste(BLACK, (0, 0, buffer.width, buffer.height))

    def refresh_time(self):
        now = datetime.datetime.now().time()
        hour = str(now.minute).zfill(2) # TODO: change back
        minute = str(now.second).zfill(2)
        self.show_colon = now.microsecond < 500000
        self.time = hour + minute

    def sheet_box(self, digit, step, movein):
        if not movein:
            step += 5
        return (digit*8, step*8, digit*8+8, step*8+8)

    def should_update(self):
        self.refresh_time()
        return self.time != self.oldtime or self.show_colon != self.old_show_colon

    def has_finished(self):
        return False

    def update(self):
        if self.time != self.oldtime:
            self.update_digits()
        if self.show_colon != self.old_show_colon:
            self.update_colon()

    def update_digits(self):
        for d in enumerate(self.time):
            i = d[0]
            if self.oldtime[i] == d[1]:
                continue
            digit = int(d[1])
            insrcbox = self.sheet_box(digit, self.step, True)
            inim = self.sheet.crop(insrcbox).convert("L")
            dstbox = [8*i, 0]
            if i >= 2:
                dstbox[0] += 1
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

    def update_colon(self):
        colour = WHITE if self.show_colon else BLACK
        self.buffer.putpixel((16, 2), colour)
        self.buffer.putpixel((16, 5), colour)
        self.old_show_colon = self.show_colon
