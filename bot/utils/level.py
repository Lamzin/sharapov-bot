import time
import os
import copy


FINISH_POSITION = 16777215

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

DEPENDENCIES_SPECIAL = [
    [
        0,   1,  2,  3,  4,  5,
        6,   7,  8,  9, 10, 11,
        12, 13, 14, 15, 16, 17,
        18, 19, 20, 21, 22, 23,
    ],
    [
        5,  0,   1,  2,  3,  4,
        11, 6,   7,  8,  9, 10,
        17, 12, 13, 14, 15, 16,
        23, 18, 19, 20, 21, 22,
    ],
    [
        18, 19, 20, 21, 22, 23,
        0,   1,  2,  3,  4,  5,
        6,   7,  8,  9, 10, 11,
        12, 13, 14, 15, 16, 17,
    ]
]


class Level(object):

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

        if self.number > 3:
            time_begin = time.time()
            self.linear_system_solution()
            print 'linear solving time: ', time.time() - time_begin
        else:
            self.special_solution()
        time_begin = time.time()
        self.go_to_success()
        print 'queries time: ', time.time() - time_begin

    def go_to_success(self):
        print self.number, self.way_to_success
        patch = [
            Level.index_to_code(item)
            for item in self.way_to_success
        ]
        self.current_position = self.request_manager.get_patch(
                patch, self.number + 1 if self.number < 7 else 7)
        self.level_complete = bool(self.current_position)

    def linear_system_solution(self):
        def solve(rows, value):
            for i in range(24):
                if value & (2**i):
                    rows[23 - i] |= 2**24
            for i in range(24):
                for j in range(i, 24):
                    if rows[j] & (2**i):
                        rows[i], rows[j] = rows[j], rows[i]
                        break
                for g in range(24):
                    if g != i and rows[g] & (2**i):
                        rows[g] ^= rows[i]
            result = 0
            for i in range(24):
                if rows[i] & (2**24):
                    result |= 2**i
            return result

        ans = \
            solve(copy.copy(DEPENDENCIES[str(self.number)]), copy.copy(self.previous_position)) \
            ^ solve(copy.copy(DEPENDENCIES[str(self.number)]), 2**24 - 1)
        for i in range(24):
            if ans & (2**i):
                self.way_to_success.append(23 - i)
        self.way_to_success = self.way_to_success[::-1]

    def special_solution(self):
        self.way_to_success = []
        for i in range(24):
            if self.previous_position & (2 ** (23 - i)) == 0:
                self.way_to_success.append(DEPENDENCIES_SPECIAL[self.number - 1][i])

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
