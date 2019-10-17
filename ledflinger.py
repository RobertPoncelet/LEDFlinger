from sys import platform
linux = platform == "linux"

if not linux:
    import pygame

import threading, time, argparse, signal

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

def shutdown(signum, frame):
    comp.stop()

signal.signal(signal.SIGTERM, shutdown)

def test(comp):
    pingfunc = ping.is_phone_available_fake if args.fakeping else ping.is_phone_available
    if args.fakeping:
        open("ping/phone", "a").close()
    connected = False
    connected_previous = False

    try:
        while True:
            connected = pingfunc()
            if connected and not connected_previous:
                print("Starting composition")
                layers = [Layer(size)]
                layers[0].add_animation(ClockAnimation(None))
                comp.start(layers)
            elif connected_previous and not connected:
                print("Stopping composition")
                comp.stop()

            connected_previous = connected
            time.sleep(1.)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")

#thr = threading.Thread(target=comp.run)
#thr2 = threading.Thread(target=test, args=[comp])
#thr.start()
#thr2.start()
#thr.join()
#thr2.join()
test(comp)
if not linux:
    pygame.quit()

