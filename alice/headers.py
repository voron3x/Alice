# -*- coding: utf-8 -*-
from alice import Alice

# Headers
GENERAL_HEADERS = [
  'Connection',
  'Cache-Control',
  'Date',
  'Pragma',
  'Trailer',
  'Transfer-Encoding',
  'Upgrade',
  'Via',
  'Warning'
]
REQUEST_HEADERS = [
  'Accept',
  'Accept-Charset',
  'Accept-Encoding',
  'Accept-Language',
  'Authorization',
  'Expect',
  'From',
  'Host',
  'If-Match',
  'If-Modified-Since',
  'If-None-Match',
  'If-Range',
  'If-Unmodified-Since',
  'Max-Forwards',
  'Proxy-Authorization',
  'Range',
  'Referer',
  'TE',
  'User-Agent'
]
RESPONSE_HEADERS = [
  'Accept-Ranges',
  'Age',
  'ETag',
  'Location',
  'Proxy-Authenticate',
  'Retry-After',
  'Server',
  'Vary',
  'WWW-Authenticate'
]
ENTITY_HEADERS = [
  'Allow',
  'Content-Encoding',
  'Content-Language',
  'Content-Length',
  'Content-Location',
  'Content-MD5',
  'Content-Range',
  'Content-Type',
  'Expires',
  'Last-Modified'
]
WEBSOCKET_HEADERS = [
  'Sec-WebSocket-Accept',
  'Sec-WebSocket-Key',
  'Sec-WebSocket-Origin',
  'Sec-WebSocket-Protocol',
  'Sec-WebSocket-Version'
]
MISC_HEADERS = ['DNT']
HEADERS  = (
      GENERAL_HEADERS
    + REQUEST_HEADERS
    + RESPONSE_HEADERS
    + ENTITY_HEADERS
    + WEBSOCKET_HEADERS
    + MISC_HEADERS
)

#Lowercase headers
NORMAL_CASE_HEADERS = dict()
for name in HEADERS:
    NORMAL_CASE_HEADERS[name.lower()] = name

class Headers(Alice):
    """ Headers is a container and parser for HTTP headers """
    def __init__(self, headers=None, *args, **kwargs):
        if headers is None:
            self.headers = dict()

        super().__init__(*args, **kwargs)

    def add(self, name, *args):
        # Make sure we have a normal case entry for name
        lcname = name.lower()
        if not NORMAL_CASE_HEADERS.get(lcname):
            NORMAL_CASE_HEADERS[lcname] = name

        name = lcname

        #Add lines
        self.headers[name] = args

        return self

    def header(self, name, *args):
        # Replace
        if args:
            return self.add(name, *args)

        if not self.headers[name.lower()]: return

        return self.headers[name.lower()]


