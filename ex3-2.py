from enum import Enum


class Result(Enum):
    insert = 0
    hit = 1
    repace = 2


class PageStatus:
    def __init__(self, code):
        self.code = code
        self.A = 0

    def __repr__(self):
        return '{}({}) '.format(self.code, self.A)


class MemoryPage:
    pointer = 0

    def __init__(self, size):
        self.maxsize = size
        self.pages = [None] * size
        self.pointer = 0

    def move_pointer(self,confirm = True):
        pointer = (self.pointer + 1) % (self.maxsize)
        if confirm:
            self.pointer = pointer
        return pointer

    def match(self):
        if not self.pages[self.move_pointer(False)]:
            return False
        if self.pages[self.pointer].A == 0:
            return True
        else:
            self.pages[self.pointer].A = 0
            return False

    def check_exsit(self, page):
        for i in range(0, self.maxsize):
            if self.pages[i] and self.pages[i].code == page:
                self.pages[i].A = 1
                return True
        return False

    def get(self, page):
        if not self.pages[self.pointer]:
            self.insert(page)
            return Result.insert

        if self.check_exsit(page):
            return Result.hit

        if not self.pages[self.pointer]:
            self.insert(page)
            return Result.insert

        if self.match():
            self.insert(page)
            return Result.repace
        else:
            self.move_pointer()
            return self.get(page)

    def disp(self):

        i = self.pointer - 1
        while i-1!=self.pointer - 1:
            if i == -1:
                i = self.maxsize - 1
            print(self.pages[i])
            i -= 1
        print(self.pages[i])

    def insert(self, page):
        self.pages[self.pointer] = PageStatus(page)
        self.move_pointer()

if __name__ == '__main__':
    x = input('Please input size:\n')
    y = MemoryPage(int(x))
    print('Input exit to exit!')
    print('Input disp to display!')
    while 1:
        inp = input('Enter page code :\n')
        if inp == 'exit':
            exit()
        if inp == 'disp':
            y.disp()
        else:
            print('\033[94m' + str(y.get(int(inp))) + '\033[0m')

