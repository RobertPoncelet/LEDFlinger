from sys import platform
linux = platform == "linux"

if not linux:
    import pygame

from compositor import Compositor
from layer import Layer
from animation import *

screen_width = 32
screen_height = 8
size = (screen_width, screen_height)
comp = Compositor(size)

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
comp.layers = layers

comp.run()

