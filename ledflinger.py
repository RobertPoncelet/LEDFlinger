from sys import platform
linux = platform == "linux"

if not linux:
    import pygame

import threading

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

def test(comp):
    msg = input()
    print("input! " + msg)
    comp.lock.acquire()
    print("lock acquired")
    layers[2].add_animation(TextAnimation(None, msg))
    layers[0].add_animation(CircleAnimation(None, WHITE, (0, screen_height), (screen_width, 0)))
    comp.lock.release()
    print("lock released")
    msg = input()
    comp.lock.acquire()
    print("lock acquired")
    comp.done = True
    comp.lock.release()
    print("lock released")

thr = threading.Thread(target=comp.run, daemon=True)
thr2 = threading.Thread(target=test, args=[comp])
thr.start()
thr2.start()
thr.join()
thr2.join()
pygame.quit()
print("all done!")

