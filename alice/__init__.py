# -*- coding: utf-8 -*-
"""
    Alice
    ~~~~~

    Alice Веб фрэймворк поддерживающий fcgi wcgi.

"""
__version__ = '0.1-dev'

class AliceBase(object):
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

class Alice(AliceBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
