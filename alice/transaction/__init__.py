# -*- coding: utf-8 -*-
from alice import Alice

class Transaction(Alice):
    def __init__(self,connection = None, *args, **kwargs):
        self.connection = connection
        super().__init__(*args, **kwargs)

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
