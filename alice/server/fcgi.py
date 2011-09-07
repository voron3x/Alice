# -*- coding: utf-8 -*-

from alice.server import Server
import socket
import struct
import sys
import errno

TYPES = [
    "BEGIN_REQUEST",
    "ABORT_REQUEST",
    "END_REQUEST",
    "PARAMS",
    "STDIN",
    "STDOUT",
    "STDERR",
    "DATA",
    "GET_VALUES",
    "GET_VALUES_RESULT",
    "UNKNOWN_TYPE"
]
TYPE_NUMBERS = dict(zip(TYPES, range(1,len(TYPES))))

ROLES = [
    "RESPONDER",
    "AUTHORIZER",
    "FILTER",
]
ROLE_NUMBERS = dict(zip(ROLES, range(1,len(ROLES))))

if __debug__:
    import time

    # Set non-zero to write debug output to a file.
    DEBUG = 0
    DEBUGLOG = '/tmp/fcgi.log'

    def _debug(level, msg):
        """ 
        Дебаг утилитка принимает на вход два параметра 
        первый цифра уровня логирования, второй строка сообщения
        """
        if DEBUG < level:
            return

        try:
            #f = open(DEBUGLOG, 'a')
            #f.write('%sfcgi: %s\n' % (time.ctime()[4:-4], msg))
            print('%sfcgi: %s\n' % (time.ctime()[4:-4], msg))
            #f.close()
        except:
            pass

class ValueEnd(Exception):
    pass

class FastCGI(Server):
    def __init__(self, host='127.0.0.1', port=6000, listen=None, *args, **kwargs):
        self.host = host
        self.port = port
        self.listen = listen
        super().__init__(*args, **kwargs)

    def accept_connection(self):
        if not self.listen:
            s = None
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                # Разрешаем выполнять bind() даже в случае, 
                # если другая программа недавно слушала тот же порт. 
                # Без этого, программа не сможет работать с портом в течение 
                # 1-2 минут после окончания работы с тем же портом в 
                # ранее запущенной программе.
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            except socket.error as msg:
                print('could not open socket: ' + str(msg))
                print(msg)
                sys.exit(1)

            try:
                s.bind((self.host, self.port))
                s.listen(5)
            except socket.error as msg:
                print('could not open socket: ' + str(msg))
                s.close()
                sys.exit(1)

            self.listen = s

        return self.listen.accept()

    def read_request(self,c):
        if __debug__: _debug(9, 'Read FCGI Request')
        #Transaction
        tx = self.application.on_transaction
        tx.connection = c
        req = tx.req

        try:
            (type, id, body) = self.read_record(c)
        except ValueEnd:
            return

        if not type and type != 'BEGIN_REQUEST':
            print("ERROR First FastCGI record wasn't a begin request.")

        self.fcgi_id = id
        
        role, flags = struct.unpack('!HB5x', body)

        self.fcgi_role = self.role_name(role)

        #Slurp 
        buffer = bytearray()
        env = dict()
        while True:
            try:
                (type, id, body) = self.read_record(c)
            except ValueEnd:
                break
            
            # Wrong id
            if self.fcgi_id != id: continue
            
            #Parse params key value
            if type == 'PARAMS':
                if body:
                    buffer += body
                    continue

                #params done
                while len(buffer):
                    name_len  = self._nv_length(buffer)
                    value_len = self._nv_length(buffer)

                    name = buffer[:name_len]
                    buffer[:name_len] = []
                    
                    value = buffer[:value_len]
                    buffer[:value_len] = []

                    env[name.decode(encoding='utf-8')] = value.decode(encoding='utf-8')
                    if __debug__: _debug(9, 'FastCGI param: {0} - {1}'.format(name, value))

                    # Store connection information
                    if 'REMOTE_ADDR' in name.decode():
                        tx.remote_address = value.decode() 

                    if 'SERVER_PORT' in name.decode():
                        tx.local_port = value.decode() 
                    

            elif type == 'STDIN':
                #Environment
                req.parse(env)

                #EOF
                if not body: break

                #Chunk
                req.parse(body)

        return tx

    def read_record(self,c):
        if not c: raise ValueEnd
        
        header = self._read_chunk(c)
        if not header: raise ValueEnd
            
        #big endian in network notation
        (version, type, id, clen, plen) = struct.unpack('!BBHHBx', header)

        body = self._read_chunk(c, clen + plen)
        
        # No content, just paddign bytes
        if not clen: body = None
        
        # Ignore padding bytes
        if plen: body = body[:clen]

        if __debug__: _debug(9, "Reading FastCGI record: {0} - {1} - {2}.".format(self.type_name(type), id, body))

        return self.type_name(type), id, body
    
    def type_name(self,number):
        return TYPES[number - 1]

    def type_number(self, name):
        return TYPE_NUMBERS[name]

    def role_name(self,number):
        return ROLES[number - 1]
    
    def role_number(self, name):
        return ROLE_NUMBERS[name]

    def write_response(self, tx):
        if __debug__: _debug(9,"Writing FCGI response")

        c = tx.connection
        
        #Headers
        chunk = """Content-Type: text/plain
Date: Tue, 30 Aug 2011 08:34:49 GMT
Status: 200 OK
Server: Alice 0.1
Content-Length: 6

"""
        self.write_record(c, 'STDOUT', self.fcgi_id, bytes(chunk, "utf-8"))

        #Body
        chunk = "hahaha"
        self.write_record(c, 'STDOUT', self.fcgi_id, bytes(chunk,"utf-8"))

        #End
        self.write_record(c, 'STDOUT', self.fcgi_id, bytes('',"utf-8"))
        self.write_record(c, 'END_REQUEST', self.fcgi_id, struct.pack('!LB3x',0,0))

    def write_record(self, c, type, id, body=None):
        if not c and not type and not id: return
        
        #Write records
        empty = 1 if not body else 0
        body_len = len(body)

        if body_len or empty:
            # Need to split content
            payload_len = 32 * 1024 if body_len > (32 * 1024) else body_len
            pad_len = (8 - (payload_len % 8)) % 8

            if __debug__: _debug(9, "Writing FastCGI record: {0} - {1} - {2}".format(type, id, body))

            #Send header
            header = struct.pack('!BBHHBx', 
                1, 
                self.type_number(type), 
                id, 
                payload_len, 
                pad_len
            )
            self._sendall(c, header)
            if body_len:
                self._sendall(c, body)
            if pad_len:
                self._sendall(c, bytes('\x00'*pad_len,"utf-8"))
            

    def run(self):
        #preload application
        app = self.app()
        app.on_transaction.test()
        
        try:
            while True:
                #Accept connection
                c, address = self.accept_connection()

                #Request
                tx = self.read_request(c)

                #Handle request via app
                self.on_request(tx)

                #Response
                self.write_response(tx)

                #finish transaction
                #self.on_finish(tx)

                #End connection
                c.close()
        finally:
            #Close socket
            self.listen.close()

        return

    def _sendall(c, data):
        """
        Writes data to a socket and does not return until all the data is sent.
        """
        length = len(data)
        while length:
            sent = c.send(data)
            data = data[sent:]
            length -= sent
    _sendall = staticmethod(_sendall)

    def _read_chunk(c,length=8):
        """
        Read chunk from socket

        Arguments:
            c - socket handler
            length - lenght of byte to read, default 8 byte

        Return: 
            a few byte
        """
        chunk = bytearray()
        while len(chunk) < length:
            buffer = bytearray(length)
            #buffer = None
            try:
                read = c.recv_into(buffer,(length - len(chunk)))
            except c.error as e:
                if e[0] == errno.EAGAIN or e[0] == errno.EINTR or errno.EWOULDBLOCK:
                    continue

            if not read: #EOF
                break
            chunk += buffer
        return chunk
    _read_chunk = staticmethod(_read_chunk)

    def _nv_length(buffer):
        # Try first byte
        len = struct.unpack('!B', buffer[:1])[0]
        buffer[:1] = []
        
        # 4 byte length
        if len & 0x80:
            chunk  = buffer[:3]
            buffer[:3] = []

            len = struct.pack('!B', len)[0]
            chunk = len + chunk

            len = struct.unpack('!L', chunk)[0]


    #    print(len)
        return len
    _nv_length = staticmethod(_nv_length)

    class FCGIProcManager(object):
        """ Класс для обработки многопроцесной обработки FCGI соеденений"""
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

