from enum import Enum


class Color:
    yellow = '\033[93m'
    blue = '\033[94m'
    purple = '\033[35m'
    end = '\033[0m'


class Status(Enum):
    busy = True
    free = False


class Progress:
    def __init__(self, start, size):
        self.start = start
        self.size = size
        self.status = Status.busy


class CheckPoint:
    start = None
    size = None

    def __init__(self, start, size):
        self.start = start
        self.size = size

    def __lt__(self, other):
        return self.size < other.size

    def __repr__(self):
        return "Checkpoint{} len:{}|".format(self.start, self.size)


class Memory:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.memory = [Status.free] * maxsize
        self.tasklist = []

    def check_empty_size(self, start, need):
        for i in range(start, start + need):
            if self.memory[i] == Status.busy:
                return False
        return True

    def set_memory(self, start, need, status):
        for i in range(start, start + need):
            self.memory[i] = status

    def get_free_area(self, size):
        checkpoints = []
        free_len = 0
        for i in range(0, self.maxsize):
            if self.memory[i] == Status.free:
                free_len += 1
            if self.memory[i] == Status.busy or i == self.maxsize - 1:
                if free_len >= size:
                    checkpoints.append(CheckPoint(i - size, free_len))
                    free_len = 0
        return checkpoints

    def recycle(self, proc_code):
        start = self.tasklist[proc_code].start
        end = self.tasklist[proc_code].size + start
        self.tasklist[proc_code].status = Status.free
        for i in range(start, end):
            self.memory[i] = Status.free
        print(Color.yellow + "Success delete Process code:{} at {}".format(proc_code, start) + Color.end)

    def ff_insert(self, size):
        for i in range(0, self.maxsize):
            if self.memory[i] == Status.free:
                if self.check_empty_size(i, size):
                    self.set_memory(i, size, Status.busy)
                    new_pro = Progress(i, size)
                    self.tasklist.append(new_pro)
                    print(Color.blue + "(FF) Success Insert Process at memory {} to {}".format(i, i + size) + Color.end)
                    return

    def bf_insert(self, size):
        checkpoints = self.get_free_area(size)
        checkpoints.sort(reverse=True)
        if not len(checkpoints):
            print('Operation Fail: No Free Memory')
            return
        start = checkpoints[0].start
        self.set_memory(start, size, Status.busy)
        self.tasklist.append(Progress(start, size))
        print(Color.blue + "(BF) Success Insert Process at memory {} to {}".format(start, start + size) + Color.end)

    def wf_insert(self, size):
        checkpoints = self.get_free_area(size)
        checkpoints.sort()
        if not len(checkpoints):
            print('Operation Fail: No Free Memory')
            return
        start = checkpoints[0].start
        self.set_memory(start, size, Status.busy)
        self.tasklist.append(Progress(start, size))
        print(Color.blue + "(WF) Success Insert Process at memory {} to {}".format(start, start + size) + Color.end)

    def disp_proc(self):
        print(Color.purple + '---display---')
        for i in range(0, len(self.tasklist)):
            print('code:{}  start:{}  size:{}  status:{}'.format(i, self.tasklist[i].start, self.tasklist[i].size,
                                                                 self.tasklist[i].status))
        print(Color.end)

    def disp_mem(self):
        pass


def instroduce():
    print('请选择你要的操作')
    print('1 FF_insert')
    print('2 BF_insert')
    print('3 WF_insert')
    print('4 recycle')
    print('5 display tasks list')
    print('6 exit')


if __name__ == '__main__':
    size = input('请输入存储总空间:')
    x = Memory(int(size))
    while 1 :
        instroduce()
        choice = int(input('请选择:'))
        if choice == 1:
            size = int(input('Enter Progress Size:'))
            x.ff_insert(size)

        elif choice == 2:
            size = int(input('Enter Progress Size:'))
            x.bf_insert(size)

        elif choice == 3:
            size = int(input('Enter Progress Size:'))
            x.wf_insert(size)

        elif choice == 4:
            size = int(input('Enter Progress Code:'))
            x.recycle(size)
        elif choice == 5:
            x.disp_proc()

        elif choice == 6:
            exit()
        else:
            print("Command Error")

