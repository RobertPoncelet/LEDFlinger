from PIL import Image, ImageFont, ImageDraw, ImageChops

def buffer(size):
    return Image.new("1", size, 0)
