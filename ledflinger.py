import threading, time, argparse, signal

import ping
from compositor import Compositor
from event_handler import EventHandler
#from layer import Layer
#from animation import *
#from clock import ClockAnimation, ClockIntroAnimation, ClockOutroAnimation
#from message import MessageAnimation

parser = argparse.ArgumentParser(description='LEDFlinger arguments',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--fakeping', type=bool, default=False, help='Instead of actually checking the wifi status, ' \
    'check for the existence of a file called ping/phone')
parser.add_argument('--minsec', type=bool, default=False, help='Show minutes/seconds instead of hours/minutes')
args = parser.parse_args()

screen_width = 32
screen_height = 8
size = (screen_width, screen_height)

comp = Compositor(size)
handler = EventHandler(comp, args.minsec)

def shutdown(signum, frame):
    #comp.stop()
    handler.stop(wait_for_finish=False)

signal.signal(signal.SIGTERM, shutdown)

def test(handler):
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
                handler.start()
                handler.clock_start()
            elif connected_previous and not connected:
                print("Stopping composition")
                handler.clock_stop()
                handler.stop()
            connected_previous = connected
            time.sleep(1.)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")

test(handler)

