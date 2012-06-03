# сoding: utf-8
"""
    path.py
    Класс работы с path частью урла
    path = Path('/foo/bar')
    str(path)
"""

from alice.utils import url_escape, url_unescape

class Path:
    def __init__(self, path):
        self.leading_slash = False
        self.trailing_slash = False
        self.parts = list()
        self.parse(path)

    def parse(self, path):
        path = url_unescape(path)

        if path[0] == '/':
            self.leading_slash = True
            path = path[1:]

        if path[-1] == '/':
            self.trailing_slash = True
            path = path[:-1]

        self.parts = path.split('/')

    def __str__(self):
        parts = [url_escape(str) for str in self.parts]
        path = '/'.join(parts)

        if self.leading_slash:
            path = '/' + path

        if self.trailing_slash:
            path = path + '/'

        return path

