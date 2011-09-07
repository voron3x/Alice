# -*- coding: utf-8 -*-
from alice import Alice

class Headers(Alice):
    """ Headers is a container and parser for HTTP headers """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def header(self, name, value):
        print(name + " = " + value)

    
