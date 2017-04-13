
import socket
import keyboard
import datetime
import time
from contextlib import contextmanager
from functools import reduce
import random

__author__ = 'Наумов Александр Сергеевич'

SERVICE_OPERATIONS = {
    0: 'power on',
    1: 'reboot',
    2: 'power off',
    3: 'sensor activated',
    4: 'blocked, encashment is required',
}


class Transaction:
    def __init__(self, data, owner):
        self.date_time = datetime.datetime.now()
        self.owner = owner
        self.owner.transaction_id += 1
        self.data = [ord(char) for char in data]
        self.types = {
            0: self.service_operation,
            1: self.monetary_operation,
            2: self.monetary_operation
        }
        self.bytes = b'zz' + owner.host_ip_to_bytes()
        self.set_transaction_bytes()

    def datetime_to_bytes(self):
        date_int = self.date_time.year % 100 << 9 | \
                   self.date_time.month << 5 | \
                   self.date_time.day & 0x1F
        _time = self.date_time.time()
        _seconds = _time.hour * 3600 + _time.minute * 60 + _time.second
        return date_int.to_bytes(2, 'big') + _seconds.to_bytes(3, 'big')

    def set_transaction_bytes(self):
        _type = self.data[0] % len(self.types)
        self.bytes += self.datetime_to_bytes()
        self.bytes += self.owner.transaction_id.to_bytes(4, 'big')
        self.bytes += _type.to_bytes(1, 'big')
        self.types[_type]()

    def service_operation(self):
        self.bytes += (self.data[1] % 5).to_bytes(1, 'big')

    def monetary_operation(self):
        _payment = reduce(lambda x, y: x * y, self.data[1:]) & 2**96-1
        self.bytes += (_payment >> 64).to_bytes(4, 'big')
        self.bytes += (_payment & 2**64-1).to_bytes(8, 'big')

    # def encashment(self):
    #     _encashment = reduce(lambda x, y: x * y, self.data[1:]) & 2**96-1
    #     self.bytes += (_encashment >> 64).to_bytes(4, 'big')
    #     self.bytes += (_encashment & 2**64-1).to_bytes(8, 'big')


class KeyboardLogger:
    def __init__(
            self, client,
            data_start=chr(random.randint(ord('a'), ord('z'))),
            max_buffer_length=15
    ):
        self.client = client
        self.max_buffer_length = max_buffer_length
        self.buffer = []
        self.data_start = data_start
        keyboard.on_press(self.keyboard_event)

    def keyboard_event(self, event):
        if not self.buffer and event.name == self.data_start:
            self.buffer.append(self.data_start)
            keyboard.unhook_all()
            keyboard.on_press(self.read_data)

    def read_data(self, event):
        if len(self.buffer) < self.max_buffer_length+1:
            if len(event.name) == 1:
                self.buffer.append(event.name)
            elif event.name == 'esc':
                self.reset()
        else:
            keyboard.unhook_all()
            self.client.start_transaction(self.buffer[1:])
            self.reset()
            keyboard.on_press(self.keyboard_event)

    def reset(self):
        self.buffer = []


class Client:
    def __init__(
            self, server_url='localhost', port_range=range(9000, 10000),
            key_request=b'OK', key_response=b'OK'
    ):
        self.server_url = server_url
        self.key_request = key_request
        self.key_response = key_response
        self.server_port = None
        self.host_ip = self.get_host_by_name()
        self.find_port(port_range)
        if self.server_port is None:
            raise socket.error
        self.host_name = socket.gethostname()
        self.get_transaction_id()
        self.keylogger = KeyboardLogger(self)

    def find_port(self, port_range):
        for server_port in port_range:
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.settimeout(0.002)
            try:
                _socket.connect((self.server_url, server_port))
                _socket.send(self.key_request)
                _response = _socket.recv(2)
            except (socket.timeout, OSError):
                _socket.close()
            else:
                if _response == self.key_response:
                    self.server_port = server_port

    def get_transaction_id(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect((self.server_url, self.server_port))
        _socket.send(b'transaction_id')
        _socket.send(self.host_ip_to_bytes())
        _response = _socket.recv(4)
        self.transaction_id = int.from_bytes(_response, 'big')

    def get_host_by_name(self):
        # return socket.gethostbyname(self.host_name)
        return '.'.join((str(random.randint(1, 254)) for _ in range(2)))

    def host_ip_to_bytes(self):
        _ip_list = self.host_ip.split('.')
        return reduce(
            lambda x, y: x + y,
            (int(item).to_bytes(1, 'big') for item in _ip_list)
        )

    def send_transaction(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.send(self.transaction.bytes)
        self.close()
        # self.socket.connect((self.server_url, self.server_port))
        # self.socket.send(self.transaction.bytes)
        # self.socket.close()

    def start_transaction(self, data):
        self.transaction = Transaction(data, self)
        self.send_transaction()

    def connect(self):
        self.socket.connect((self.server_url, self.server_port))

    def close(self):
        self.socket.close()

    def send(self, data):
        self.socket.send(data)


if __name__ == '__main__':

    t1 = Client()
    while True:
        time.sleep(60)
