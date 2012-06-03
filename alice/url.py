# coding: utf-8
"""
Uniform Resource Locator

"""

from alice.utils import url_escape, url_unescape
import re

# Characters (RFC 3986)
UNRESERVED = 'A-Za-z0-9\-\.\_\~'
SUBDELIM   = '!\$\&\'\(\)\*\+\,\;\='
PCHAR      = UNRESERVED + SUBDELIM + '\%\:\@'

class URL:
    def __init__(self, url=None):
        self.url = url
        self.fragment = None
        self.host = None
        self.port = None
        self.scheme = None
        self.userinfo = None

        if self.url is not None:
            self.parse(url)

    @property
    def base(self):
        return URL()

    def ihost(self, host=None):
        #Set
        if host:
            self.host = host.decode("idna")
            return self.host

        return self.host.encode("idna")

    def authority(self, authority):
        """ Authority part of this URL. """
        #Set
        if authority:
            host = authority

            # Userinfo
            match = re.search(r'^([^\@]+)\@(.+)$', authority)
            if match:
                self.userinfo = url_unescape(match.group(1))
                host = match.group(2)

            # Port
            match = re.search(r'^(.+)\:(\d+)$', host)
            if match:
                host = match.group(1)
                self.port = match.group(2)

            # Host
            host = url_unescape(host)
            match = re.search('[^\x00-\x7f]',host)
            if match:
                self.host = host.decode("idna")
                return self.ihost(host)

            self.host = host
            return self.host

    def parse(self,url):
        """ Parse URL. """
        assert url is not None, "Url must be defined"
        # Official regex
        match = re.search('(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*)(?:\?([^#]*))?(?:#(.*))?', url)
        scheme, authority, path, query, fragment = match.groups()

        self.scheme = scheme
        self.authority(authority)




