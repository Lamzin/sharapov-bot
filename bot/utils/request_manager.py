import requests
import gevent
from gevent.pool import Pool
from gevent.queue import Queue

from threading import Thread


class RequestManager(object):

    SOURCE = u'http://teorver.pp.ua/ukr/games/klumba/index.php'

    def __init__(self):
        self.session = requests.session()
        from gevent import monkey
        monkey.patch_all()

    def get(self, code=None, timeout=10):
        url = RequestManager.SOURCE
        if code:
            url += u'?code={}'.format(code)
        try:
            request = self.session.get(url, timeout=timeout)

            html = request.text
            return html
        except Exception as e:
            pass

    def post_name(self):
        url = u'http://teorver.pp.ua/ukr/games/klumba/finish.php'
        data = {
            'name': "Lamzin bot"
        }
        request = self.session.post(url, data=data)

        return request.text

    def get_patch(self, patch):
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

        ths = []
        for code in patch:
            th = Thread(target=self.get, args=(code,))
            th.start()
            ths.append(th)

        for th in ths:
            th.join()
