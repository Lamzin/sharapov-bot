import time
import requests
import Queue

from threading import Thread
from parser import Parser


TIMEOUT_GET = 0.15
TIMEOUT_GET_PATCH = 0.15
TIME_CHECK_QUEUE = 0.025
TIMEOUT_PATCH = 0.3


class RequestManager(object):

    SOURCE = u'http://teorver.pp.ua/ukr/games/klumba/index.php'

    def __init__(self):
        self.session = requests.session()

    def post_name(self):
        try:
            url = u'http://teorver.pp.ua/ukr/games/klumba/finish.php'
            data = {
                'name': "Lamzin bot"
            }
            request = self.session.post(url, data=data)
            return request.text
        except Exception as e:
            print repr(e)

    def get(self, code=None):
        url = RequestManager.SOURCE
        if code:
            url += u'?code={}'.format(code)
        try:
            request = self.session.get(url, timeout=TIMEOUT_GET)
            html = request.text
            return html
        except Exception:
            pass

    def get_patch_worker(self, code, queue, expected_level):
        url = u'{}?code={}'.format(RequestManager.SOURCE, code)
        try:
            request = self.session.get(url, timeout=TIMEOUT_GET_PATCH)
            p = Parser()
            p.parse(request.text)
            if p.level == expected_level:
                queue.put_nowait(p.flowers)
        except Exception:
            pass

    def get_patch(self, patch, expected_level):
        def thread_way():
            for code in patch:
                th = Thread(target=self.get_patch_worker, args=(code, response_queue, expected_level))
                th.start()

        response_queue = Queue.Queue()
        time_begin = time.time()
        thread_way()
        while response_queue.empty():
            if time.time() - time_begin > TIMEOUT_PATCH:
                return None
            time.sleep(TIME_CHECK_QUEUE)

        return response_queue.get_nowait()
