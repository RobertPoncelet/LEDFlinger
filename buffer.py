from PIL import Image

def buffer(size):
    return Image.new("1", size, 0)
