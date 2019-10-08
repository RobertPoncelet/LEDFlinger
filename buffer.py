from sys import platform
linux = platform == "linux"

if linux:
    from PIL import Image, ImageFont, ImageDraw, ImageChops
else:
    import pygame


def buffer(size):
    if linux:
        return Image.new("1", size, 0)
    else:
        return pygame.Surface(size)
