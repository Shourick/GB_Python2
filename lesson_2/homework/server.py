
# Сервер платёжного терминала

import socketserver
import datetime

__author__ = 'Наумов Александр Сергеевич'


class MemTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(2).decode('utf-8')
        if self.data != 'zz':
            print(
                "Клиент {} сообщает {}".
                format(self.client_address[0], self.data)
            )
            if self.data == 'OK':
                self.request.send(bytes('OK', 'utf-8'))
            else:
                print('Неизвестный запрос')
        else:
            self.server.received_data(self.request.recv(18))


SERVICE_OPERATIONS = {
    0: 'power on',
    1: 'reboot',
    2: 'power off',
    3: 'sensor activated',
    4: 'blocked, encashment is required',
}


class Transaction:
    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.bytes_to_ip()
        self.bytes_to_datetime()
        self.bytes_to_operation_type()
        self.bytes_to_id()
        self.amount = None

    def bytes_to_ip(self):
        self.client_ip = '.'.join((str(byte) for byte in self.byte_data[:4]))

    def bytes_to_datetime(self):
        _year = (self.byte_data[4] >> 1) + \
                datetime.date.today().year // 100 * 100
        _month = int.from_bytes(self.byte_data[4:6], 'big') & 0x1E0 >> 5
        _day = int.from_bytes(self.byte_data[4:6], 'big') & 0x1F
        _seconds = int.from_bytes(self.byte_data[6:9], 'big')
        m, s = divmod(_seconds, 60)
        h, m = divmod(m, 60)
        self.date_time = datetime.datetime(_year, _month, _day, h, m, s)

    def bytes_to_operation_type(self):
        self.operation = self.byte_data[9]

    def bytes_to_id(self):
        self.id = int.from_bytes(self.byte_data[10:14], 'big')


class MonetaryTransaction(Transaction):
    def __init__(self, byte_data):
        super().__init__(byte_data)
        self.bytes_to_amount()

    def bytes_to_amount(self):
        self.amount = int.from_bytes(self.byte_data[14:], 'big') / 100


class Server(socketserver.TCPServer):
    def __init__(self, server_ip='localhost', server_port=9999):
        super().__init__((server_ip, server_port), MemTCPHandler)

    def received_data(self, byte_data):
        self.transaction = Transaction(byte_data)
        if 2 >= self.transaction.operation >= 1 :
            self.transaction = MonetaryTransaction(byte_data)
        elif self.transaction.operation != 0:
            raise ValueError('Wrong operation type!')
        print(
            'Terminal ip:{}\nDate: {}\nOperation type: {}\nId: {}\nAmount: {}'
            .format(
                self.transaction.client_ip,
                self.transaction.date_time,
                self.transaction.operation,
                self.transaction.id,
                self.transaction.amount
            )
        )




if __name__ == '__main__':
    # HOST, PORT = 'localhost', 9999
    # server = socketserver.TCPServer((HOST, PORT), MemTCPHandler)
    server = Server()
    print('Testing server is running')

    server.serve_forever()

