from enum import Enum


class Status(Enum):
    using = True
    empty = False


class Memory:
    def __init__(self,maxsize):
        self.maxsize = maxsize
        self.memory = [Status.empty] * maxsize
        print(self.memory)

    def check_empty_size(self, start, need):
        for i in range(start, start + need):
            if self.memory[i] == Status.using:
                return False
        return True

    def set_memory_used(self, start, need):
        for i in range(start, start + need):
            self.memory[i] = Status.using

    def ff_insert(self, size):
        for i in range(0, len(self.memory)):
            if self.memory[i] == Status.empty:
                if self.check_empty_size(i, size):
                    self.set_memory_used(i, size)
                    print("Success Insert Process at memory {} to {}".format(i, i + size))
                    return

    def bf_insert(self, size):
        pass

    def wf_insert(self, size):
        pass


x = Memory(20)
x.ff_insert(20)
