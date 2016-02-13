import time
import requests
import gevent
from gevent.pool import Pool
from gevent.queue import Queue

from threading import Thread
from Queue import Queue
from parser import Parser


class RequestManager(object):

    SOURCE = u'http://teorver.pp.ua/ukr/games/klumba/index.php'

    def __init__(self):
        self.session = requests.session()
        from gevent import monkey
        monkey.patch_all()

    def get(self, code=None):
        url = RequestManager.SOURCE
        if code:
            url += u'?code={}'.format(code)
        try:
            request = self.session.get(url, timeout=0.5)

            html = request.text
            return html
        except Exception as e:
            pass

    def get_path_worker(self, code, queue, expected_level):
        url = u'{}?code={}'.format(RequestManager.SOURCE, code)
        try:
            request = self.session.get(url, timeout=0.5)
            p = Parser()
            p.parse(request.text)
            if p.level == expected_level:
                queue.put_nowait(p.flowers)
        except Exception:
            pass

    def post_name(self):
        url = u'http://teorver.pp.ua/ukr/games/klumba/finish.php'
        data = {
            'name': "Lamzin bot"
        }
        request = self.session.post(url, data=data)

        return request.text

    def get_patch(self, patch, expected_level):
        # workers = len(patch)
        # workers = 3
        # pool = Pool(workers)
        # queue = Queue(24)
        #
        # for item in patch:
        #     queue.put(item)
        # queue.put(StopIteration)
        #
        # for item in queue:
        #     pool.spawn(self.get, item)
        # pool.join()

        time_begin = time.time()
        queue = Queue()
        for code in patch:
            th = Thread(target=self.get_path_worker, args=(code, queue, expected_level))
            th.start()

        while queue.empty():
            if time.time() - time_begin > 0.2:
                break
            time.sleep(0.01)

        return queue.get_nowait()
