# coding: utf-8

import urllib.parse
import encodings.idna

def url_unescape(string):
    """
    return unescaped URL
    url_unescape(string)
    """
    return urllib.parse.unquote(string, encoding='utf-8')

def url_escape(string):
    """
    return escaped URL
    url_escape(string)
    """
    return urllib.parse.quote(string, encoding='utf-8')
