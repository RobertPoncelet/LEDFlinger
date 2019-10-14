from sys import platform
linux = platform == "linux"

if not linux:
    import pygame

import threading, time, argparse

import ping
from compositor import Compositor
from layer import Layer
from animation import *
from clock import ClockAnimation

parser = argparse.ArgumentParser(description='LEDFlinger arguments',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--fakeping', type=bool, default=False, help='Instead of actually checking the wifi status, ' \
    'check for the existence of a file called ping/phone instead')
args = parser.parse_args()

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
#layers[0].add_animation(CircleAnimation(None, WHITE, (0, screen_height), (screen_width, 0), waiting_for=text_anim))
#layers[1].add_animation(CircleAnimation(None, WHITE, (screen_width, 0), (0, screen_height), waiting_for=first_anim))
layers[2].add_animation(text_anim)
#layers[3].add_animation(BackgroundAnimation(None, WHITE))
comp.layers = layers

def test(comp):
    msg = input()

    with comp.lock:
        layers[2].add_animation(ClockAnimation(None))

    pingfunc = ping.is_phone_available_fake if args.fakeping else ping.is_phone_available
    while pingfunc():
        time.sleep(1.)

    with comp.lock:
        comp.done = True

thr = threading.Thread(target=comp.run, daemon=True)
thr2 = threading.Thread(target=test, args=[comp])
thr.start()
thr2.start()
thr.join()
thr2.join()
if not linux:
    pygame.quit()

