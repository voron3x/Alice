# -*- coding: utf-8 -*-
""" WSGI сервер """
from alice.server import Server

class WSGI(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, env, start_response):
        #preload application
        app = self.app()
        app.on_transaction.test()

        tx = app.on_transaction
        req = tx.req
        req.parse(env)

        #Store connection information
        tx.remote_address = env['REMOTE_ADDR']
        tx.local_port = env['SERVER_PORT']

        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [b"Hello World"]
