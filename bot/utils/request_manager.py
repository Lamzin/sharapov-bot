import requests


class RequestManager(object):

    SOURCE = u'http://teorver.pp.ua/ukr/games/klumba/index.php'

    def __init__(self):
        self.session = requests.session()

    def get(self, code=None):
        url = RequestManager.SOURCE
        if code:
            url += u'?code={}'.format(code)
        try:
            request = self.session.get(url, timeout=10)
            html = request.text
            return html
        except Exception as e:
            print e

    def post_name(self):
        url = u'http://teorver.pp.ua/ukr/games/klumba/finish.php'
        data = {
            'name': "Lamzin bot"
        }
        request = self.session.post(url, data=data)
        return request.text