from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT, CP437_FONT

from PIL import Image, ImageFont, ImageDraw, ImageChops

import time

import threading

from layer import Layer
from animation import *
from colours import BLACK, WHITE

class Compositor(object):
    def __init__(self, size):
        self.scaling_factor = 16
        self.size = size
        self.screen_width, self.screen_height = self.size
        self.layers = []
        self.wait_time = 0.1
        self.done = False
        self.waiting_for_finish = False
        self.lock = threading.Lock()
        self.debug_image = None

    def init_device(self):
        self.serial = spi(port=0, device=0, gpio=noop())
        # TODO: args
        self.device = max7219(self.serial, width=self.screen_width, height=self.screen_height,
                            block_orientation=90, cascaded=4, blocks_arranged_in_reverse_order=True)
        self.device.contrast(2)

    def save_debug_image(self):
        if self.debug_image:
            print("Saving debug image")
            self.debug_image.save("debug_image.png")
        else:
            print("No debug image to save")

    def start(self, layers):
        self.init_device()
        self.layers = layers
        self.thr = threading.Thread(target=self.run)
        self.thr.start()

    def stop(self, wait_for_finish=True):
        with self.lock:
            if wait_for_finish:
                self.waiting_for_finish = True
            else:
                self.done = True
        self.thr.join()

    def run(self):

        self.done = False
        try:
            while not self.done:

                time.sleep(self.wait_time) # TODO: replace with luma.core.sprite_system.framerate_regulator

                self.lock.acquire()

                # START COMPOSITION

                if not self.layers:
                    self.done = True

                update = False
                for layer in self.layers:
                    if layer.should_update():
                        update = True
                        break

                if update:
                    soonest_update = -1.
                    for layer in self.layers:
                        layer.update()
                        if soonest_update < 0 or layer.get_next_update() < soonest_update:
                            soonest_update = layer.get_next_update()

                    if len(self.layers) == 1:
                        im = self.layers[0].buffer
                    else:
                        im = Image.new("1", self.size, BLACK)
                        for layer in self.layers:
                            im = ImageChops.difference(im, layer.buffer)

                    self.device.display(im)
                    self.debug_image = im

                    self.wait_time = soonest_update - time.time()
                    if self.wait_time < 0:
                        self.wait_time = 0
                else:
                    # If we're not updating, we might be finished
                    if self.waiting_for_finish:
                        finished = True
                        for layer in self.layers:
                            if not layer.empty():
                                finished = False
                                break
                        if finished:
                            self.done = True
                # END COMPOSITION

                self.lock.release()

        except KeyboardInterrupt:
            pass

        self.layers = []
        self.device.cleanup()

