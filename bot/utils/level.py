import time
import subprocess
import os


DEPENDENCIES = {
    '1': [8388608, 4194304, 2097152, 1048576, 524288, 262144,
          131072, 65536, 32768, 16384, 8192, 4096,
          2048, 1024, 512, 256, 128, 64,
          32, 16, 8, 4, 2, 1],
    '2': [4194304, 2097152, 1048576, 524288, 262144,
          8388608, 65536, 32768, 16384, 8192, 4096,
          131072, 1024, 512, 256, 128, 64, 2048,
          16, 8, 4, 2, 1, 32],
    '3': [131072, 65536, 32768, 16384, 8192, 4096,
          2048, 1024, 512, 256, 128, 64,
          32, 16, 8, 4, 2, 1,
          8388608, 4194304, 2097152, 1048576, 524288, 262144],
    '4': [16648224, 16581648, 16548360, 16531716, 16523394, 16519233,
          8648736, 4453392, 2355720, 1306884, 782466, 520257,
          8523744, 4263888, 2133960, 1068996, 536514, 270273,
          8521791, 4260927, 2130495, 1065279, 532671, 266367],
    '5': [12713984, 14745600, 7372800, 3686400, 1843200, 790528,
          8587264, 4424704, 2212352, 1106176, 553088, 274496,
          134176, 69136, 34568, 17284, 8642, 4289,
          2096, 1080, 540, 270, 135, 67],
    '6': [6490112, 11764736, 14270976, 7135488, 3436672, 1585216,
          12684320, 14863888, 7563016, 3781508, 1888706, 811201,
          8586800, 4426552, 2215324, 1107662, 553799, 274819,
          134168, 69164, 34614, 17307, 8653, 4294],
    '7': [12779520, 14909440, 7454720, 3727360, 1863680, 798720,
          12782592, 14913024, 7456512, 3728256, 1864128, 798912,
          199728, 233016, 116508, 58254, 29127, 12483,
          3120, 3640, 1820, 910, 455, 195]
}


class Level(object):

    FINISH_POSITION = 16777215

    def __init__(self, request_manager, parser, number, start_position=None):
        self.request_manager = request_manager
        self.parser = parser
        self.number = number
        self.dependencies = []
        self.previous_position = start_position or self.get_start_position()
        self.current_position = []
        self.level_complete = False
        self.way_to_success = []

    @staticmethod
    def index_to_code(index):
        return (index / 6 + 1) * 10 + (index % 6 + 1)

    def get_start_position(self):
        html = self.request_manager.get()
        self.parser.parse(html)
        return self.parser.flowers

    def run(self):
        # for i in range(24):
        #     if not self.level_complete:
        #         self.find_dependencies(i)
        self.dependencies = DEPENDENCIES[str(self.number)]

        if not self.level_complete:
            time_begin = time.time()
            self.dfs()
            print 'dfs: ', time.time() - time_begin
            self.go_to_success()

    # def find_dependencies(self, index):
    #     html = self.request_manager.get(Level.index_to_code(index))
    #     self.parser.parse(html)
    #     self.current_position = self.parser.flowers
    #     if self.parser.level == self.number + 1:
    #         self.level_complete = True
    #         return
    #
    #     self.dependencies[index] = int(self.previous_position) ^ int(self.current_position)
    #     self.previous_position = self.current_position

    def go_to_success(self):
        print self.number, self.way_to_success
        for i, item in enumerate(self.way_to_success):
            if i < len(self.way_to_success) - 1:
                self.request_manager.get(Level.index_to_code(item))
            else:
                html = self.request_manager.get(Level.index_to_code(item))
                self.parser.parse(html)
                self.current_position = self.parser.flowers
                if self.parser.level == self.number + 1:
                    self.level_complete = True

    def dfs(self):
        # HACK WITH C++
        with open('input.txt', 'w') as infile:
            infile.write('{}\n'.format(self.previous_position))
            for index, value in enumerate(self.dependencies):
                infile.write('{} {}\n'.format(index, value))

        try:
            os.remove('output.txt')
        except Exception:
            pass
        os.startfile('utils\CPP\dfs.exe')

        while not os.path.isfile('output.txt'):
            time.sleep(0.001)

        with open('output.txt', 'r') as outfile:
            self.way_to_success = map(int, outfile.read().split())
        os.remove('output.txt')
        # HACK WITH C++
