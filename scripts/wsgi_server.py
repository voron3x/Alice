#!/usr/bin/env python
# vim: set fileencoding=utf-8

import sys

from wsgiref.simple_server import make_server

sys.path.append("../")

from alice.server.wsgi import WSGI
from alice.hello_world import AliceTest
wsgi = WSGI(app_class=AliceTest)

httpd = make_server('', 8000, wsgi.run)

print("Serving on port 8000...")
httpd.serve_forever()
