# -*- coding: utf-8 -*-

class Transaction:
    def __init__(self,connection = None, *args, **kwargs):
        self.connection = connection

    def remote_address(self, addr = None):
        if addr is not None:
            self.remote_address = addr
        return self.remote_address

    def test(self):
        print("Test Transaction")

    def req(self):
        pass

    def res(self):
        pass
