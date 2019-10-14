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
layers = [Layer(size)]
layers[0].add_animation(ClockAnimation(None))
with comp.lock:
    comp.layers = layers

def test(comp):
    pingfunc = ping.is_phone_available_fake if args.fakeping else ping.is_phone_available

    try:
        while True:
            time.sleep(1.)

            with comp.lock:
                comp.done = True

    except KeyboardInterrupt:
        print("KeyboardInterrupt")

thr = threading.Thread(target=comp.run)
thr2 = threading.Thread(target=test, args=[comp])
thr.start()
thr2.start()
thr.join()
thr2.join()
if not linux:
    pygame.quit()

