
import asyncio
import logging
import datetime
from models import DbWorks, Transaction

__author__ = 'Наумов Александр Сергеевич'


class Server:
    def __init__(self, server_ip='localhost', server_port=9999, _loop=None):
        self._loop = _loop or asyncio.get_event_loop()
        self._server = asyncio.start_server(
            self.handle, host=server_ip, port=server_port
        )

    def start(self, and_loop=True):
        self._server = self._loop.run_until_complete(self._server)
        logging.info(
            'Server listening on {}'
            .format(self._server.sockets[0].getsockname())
        )
        if and_loop:
            self._loop.run_forever()

    def stop(self, and_loop=True):
        self._server.close()
        if and_loop:
            self._loop.close()

    async def handle(self, reader, writer):
        peer_name = writer.get_extra_info('peername')
        logging.info('Accepted connection from {}'.format(peer_name))
        _flag = 'data'
        while True:   # not reader.at_eof():
            self.data = await reader.read(1024)
            if self.data:
                if self.data[:2] != b'zz':
                    print(
                        "Клиент {} сообщает {}".
                        format(writer.get_extra_info('peername'), self.data)
                    )
                    if self.data[:2] == b'OK':
                        writer.write(b'OK')
                    elif self.data[:14] == b'transaction_id':
                        _client_ip = '.'.join(
                            (str(byte) for byte in self.data[14:16]))
                        writer.write(
                            DbWorks().select_last_transaction(_client_ip)
                            .to_bytes(4, 'big')
                        )
                    elif self.data[:13] == b'file transfer' or _flag == 'file':
                        _flag = 'file'
                        name_length = self.data[13]
                        file_name = self.data[14:14+name_length]
                        self.data = self.data[14+name_length:]
                        with open(file_name, 'wb') as f:
                            f.write(self.data)
                            while not reader.at_eof():
                                self.data = await reader.read(1024)
                                f.write(self.data)
                    else:
                        print('Неизвестный запрос')
                else:
                    self.received_data(self.data[2:])
            else:
                print("Terminating connection")
                writer.close()
                break

    def received_data(self, byte_data):
        self.transaction = Transaction(byte_data)
        if 2 >= self.transaction.operation >= 1:
            self.transaction = MonetaryTransaction(byte_data)
        elif self.transaction.operation != 0:
            raise ValueError('Wrong operation type!')
        DbWorks().save_transaction(self.transaction)
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()

