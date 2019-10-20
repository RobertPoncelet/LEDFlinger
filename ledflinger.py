from sys import platform
linux = platform == "linux"

if not linux:
    import pygame

import threading, time, argparse, signal

import ping
from compositor import Compositor
from layer import Layer
from animation import *
from clock import ClockAnimation, ClockIntroAnimation
from message import MessageAnimation

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
            #print("ping")
            if connected and not connected_previous:
                print("Starting composition")
                layers = [Layer(size)]
                layers[0].add_animation(MessageAnimation(layers[0].buffer, "Hello"))
                clock_intro = ClockIntroAnimation(layers[0].buffer)
                layers[0].add_animation(clock_intro)
                layers[0].add_animation(ClockAnimation(layers[0].buffer, intro=clock_intro))
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

