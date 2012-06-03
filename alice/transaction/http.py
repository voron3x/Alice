# coding: utf-8
from alice.transaction.base import Transaction
from alice.message import Request, Response

class TransactionHTTP(Transaction):
    def __init__(
            self,
            req = Request(),
            res = Response(),
            *args,
            **kwargs
        ):
        self.req = req
        self.res = res
        super().__init__(*args, **kwargs)

    def test(self):
        print("HTTP Transaction test")
