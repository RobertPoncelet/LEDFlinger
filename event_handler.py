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
        self.main_layer = Layer(self.comp.size)
        self.main_layer.add_animation(MessageAnimation(self.main_layer.buffer, "Hello"))
        self.layers = [self.main_layer]
        self.comp.start(self.layers)

    def clock_start(self):
        clock_intro = ClockIntroAnimation(self.main_layer.buffer, minutes_seconds=self.minsec)
        self.main_layer.add_animation(clock_intro)

        self.clock = ClockAnimation(self.main_layer.buffer, intro=clock_intro, minutes_seconds=self.minsec)
        self.main_layer.add_animation(self.clock)

    def clock_stop(self):
        clock_outro = ClockOutroAnimation(self.main_layer.buffer, self.clock)
        self.main_layer.add_animation(clock_outro)
        self.clock.finished = True

    def stop(self, wait_for_finish=True):
        self.main_layer.add_animation(MessageAnimation(self.main_layer.buffer, "Goodnight"))
        self.comp.stop(wait_for_finish)
