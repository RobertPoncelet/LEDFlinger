from sys import platform
linux = platform == "linux"

from compositor import Compositor
from layer import Layer
from animation import *
from clock import *
from message import MessageAnimation

class EventHandler(object):
    def __init__(self, comp, minsec):
        self.comp = comp
        self.minsec = minsec

    def start(self):
        self.layers = [Layer(self.comp.size)]
        self.layers[0].add_animation(MessageAnimation(self.layers[0].buffer, "Hello"))

        clock_intro = ClockIntroAnimation(self.layers[0].buffer)
        self.layers[0].add_animation(clock_intro)

        self.clock = ClockAnimation(self.layers[0].buffer, intro=clock_intro, minutes_seconds=self.minsec)
        self.layers[0].add_animation(self.clock)

        self.comp.start(self.layers)

    def stop(self, wait_for_finish=True):
        clock_outro = ClockOutroAnimation(self.layers[0].buffer, self.clock)
        self.layers[0].add_animation(clock_outro)

        self.layers[0].add_animation(MessageAnimation(self.layers[0].buffer, "Goodnight"))
        self.layers[0].queue[0].finished = True

        self.comp.stop(wait_for_finish)
