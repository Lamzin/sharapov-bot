import time

from utils import Parser, RequestManager, Level


EXPECTED_RECORD_TIME = 0.95


class App(object):

    def __init__(self):
        self.parser = Parser()
        self.request_manager = RequestManager()

    def run(self):
        time_begin = time.time()
        try:
            position = None
            for level_number in range(1, 8):
                level = Level(self.request_manager, self.parser, level_number, position)
                level.run()

                position = level.current_position
                print level_number, level.level_complete
                if (not level.level_complete and level_number < 7) \
                        or time.time() - time_begin > EXPECTED_RECORD_TIME:
                    return False

            if time.time() - time_begin < EXPECTED_RECORD_TIME:
                print 'POSTING... #time = {}!'.format(time.time() - time_begin)
                html = self.request_manager.post_name()
                print 'POST with time = {}!'.format(time.time() - time_begin)
                return True
            print 'finish with time = {}!'.format(time.time() - time_begin)
        except Exception as e:
            print repr(e)


if __name__ == "__main__":
    # App().run()
    while True:
        if App().run():
            break
