# coding: utf-8
from alice.transaction.http import TransactionHTTP

class Application:
    def __init__(self, *args, **kwargs):
        self.on_transaction = TransactionHTTP()

    def handler():
        raise NotImplementedError('Method hendler is pure virtual')
