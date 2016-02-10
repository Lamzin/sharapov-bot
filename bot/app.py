import time

from utils import Parser, RequestManager, Level


class App(object):

    def __init__(self):
        self.parser = Parser()
        self.request_manager = RequestManager()

    def run(self):

        position = None
        for level_number in range(1, 8):
            level = Level(self.request_manager, self.parser, level_number, position)
            level.run()
            position = level.current_position
            print level_number, level.level_complete

        # html = self.request_manager.post_name()
        # print html

if __name__ == "__main__":
    time_begin = time.time()
    App().run()
    print time.time() - time_begin

