# -*- coding: utf-8 -*-

from alice import Alice

class Server(Alice):
    def __init__(self,app_class = None, *args, **kwargs):
        self.app_class = app_class
        self.application = None
        super().__init__(*args,**kwargs)

    def app(self):
        if self.application is None:
            self.application = self.app_class()
        return self.application

    def on_transaction(self):
        return self.app.on_transaction

    def on_request(self,tx):
        app = self.app()
        app.handler(tx)

    def run(self):
        raise NotImplementedError('Method run is pure virtual')

    def test(self):
        print("Test")