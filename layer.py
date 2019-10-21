import buffer
import collections, time, math

class Layer(object):
    def __init__(self, size, flags=0):
        self.buffer = buffer.buffer(size)
        self.flags = flags
        self.queue = collections.deque()
        self.update_interval = -1
        self.next_update = -1

    def add_animation(self, anim):
        anim.buffer = self.buffer # TODO: is this still needed?
        self.queue.append(anim)
        if len(self.queue) == 1:
            self.update_interval = anim.update_interval
            self.recalculate_next_update()

    def recalculate_next_update(self):
        if self.update_interval > 0 and not self.empty():
            t = time.time()
            wait = math.fmod(t, self.update_interval)
            self.next_update = t + self.update_interval - wait
        else:
            self.next_update = -1.

    def should_update(self):
        return not self.empty() and time.time() > self.next_update and self.queue[0].should_update()

    def empty(self):
        return len(self.queue) == 0

    def update(self):
        if not self.should_update():
            return
        self.queue[0].update()
        if self.queue[0].has_finished():
            self.queue.popleft()
            if not self.empty():
                self.update_interval = self.queue[0].update_interval
        self.recalculate_next_update()

    def get_next_update(self):
        return self.next_update
