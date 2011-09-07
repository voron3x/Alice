#!/usr/bin/env python
# vim: set fileencoding=utf-8

from alice.server.fcgi import FastCGI
from alice.hello_world import AliceTest

fcgi = FastCGI(host='127.0.0.1', port=6000)
fcgi.app_class = AliceTest
fcgi.run()
