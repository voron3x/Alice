# -*- coding: utf-8 -*-
import alice.headers

class Content:
    """ абстрактный класс для работы с содержимым HTTP/1.1 rfc2616 """
    def __init__(self, *args, **kwargs):
        self.headers = alice.headers.Headers()

class Single(Content):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
