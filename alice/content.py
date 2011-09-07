# -*- coding: utf-8 -*-
from alice import Alice
import alice.headers

class Content(Alice):
    """ абстрактный класс для работы с содержимым HTTP/1.1 rfc2616 """
    def __init__(self, *args, **kwargs):
        self.headers = alice.headers.Headers()
        super().__init__(*args, **kwargs)

class Single(Content):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
