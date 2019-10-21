from animation import Animation
from PIL import Image, ImageDraw, ImageFont
from colours import BLACK, WHITE

class MessageAnimation(Animation):
    def __init__(self, buffer, message, update_rate=30):
        super().__init__(buffer, update_rate)
        im = Image.new("1", (1,1))
        draw = ImageDraw.ImageDraw(im)
        font = ImageFont.truetype("/home/pi/.fonts/Perfect_DOS_VGA_437_Win.ttf", 8)
        sheet_size = draw.textsize(message, font=font)
        self.sheet = Image.new("1", sheet_size)
        draw = ImageDraw.ImageDraw(self.sheet)
        draw.text((0, 0), message, fill=WHITE, font=font)
        self.step = self.buffer.width

    def should_update(self):
        return self.step >= -self.sheet.width

    def has_finished(self):
        return not self.should_update()

    def update(self):
        self.buffer.paste(BLACK, (0, 0, self.buffer.width, self.buffer.height))
        self.buffer.paste(self.sheet, (self.step, 0))
        self.step -= 1
