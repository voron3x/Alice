# -*- coding: utf-8 -*-
"""
    Тестовые приложения
"""

from alice.application import Application

class AliceTest(Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handler(self, tx):
        print("In AliceTest - host:{0} - port:{1}".format(
            tx.remote_address, tx.local_port)
        )

        # Request
        #method = tx.req.method
        #path   = tx.req.url.path

        # Response
        #tx.res.code(200)
        #tx.res.headers.content_type('text/html')
        #tx.res.body("Ha-ha: method request for path!")

        # Resume transaction
        #tx.resume

