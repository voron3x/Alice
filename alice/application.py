# -*- coding: utf-8 -*-
from alice import Alice
from alice.transaction.http import TransactionHTTP

class Application(Alice):
    def __init__(self, *args, **kwargs):
        self.on_transaction = TransactionHTTP()
        super().__init__(*args, **kwargs)

    def handler():
        raise NotImplementedError('Method hendler is pure virtual')
