# -*- coding: utf-8 -*-
from alice import Alice
import urllib.parse
import alice.content


class Message(Alice):
    def __init__(self, *args, **kwargs):
        self.content = alice.content.Single()
        super().__init__(*args, **kwargs)

class Request(Message):
    def __init__(self, *args, **kwargs):
        self.req_method = 'GET'
        self.env = None
        super().__init__(*args, **kwargs)

    def test(self):
        print("It's a Request TEST")

    def parse(self, *args):
        #Parse CGI like environment
        if args[0] and isinstance(args[0], dict):
            self._parse_env(args[0])

    def _parse_env(self, env):
        # Make environment accessible
        self.env = env
        
        # Extract headers from environment
        headers = self.content.headers
        #url = self.url
        #base = self.base

        for name in env:
            if name.startswith('HTTP_'):
                value = env[name]
                name = name.replace('HTTP_', '', 1)
                name = name.replace('_','-')
                headers.header(name, value)

            

class Response(Message):
    def __init__(self, *args, **kwargs):
        self.response_code = 200
        super().__init__(*args, **kwargs)

    def test(self):
        print("This is test in response mrthod")

        
        
