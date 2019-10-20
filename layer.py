import buffer
import collections

class Layer(object):
    def __init__(self, size, flags=0):
        self.buffer = buffer.buffer(size)
        self.flags = flags
        self.queue = collections.deque()

    def add_animation(self, anim):
        anim.buffer = self.buffer # TODO: is this still needed?
        self.queue.append(anim)

    def should_update(self):
        return len(self.queue) > 0 and self.queue[0].should_update()

    def empty(self):
        return len(self.queue) > 0

    def update(self):
        if not self.should_update():
            return
        self.queue[0].update()
        if self.queue[0].has_finished():
            self.queue.popleft()
