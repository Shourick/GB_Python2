import asyncio
import os
import urllib.request


class Client(asyncio.Protocol):
    TIMEOUT = 1.0
    event_list = []
    for i in range(10):
        event_list.append('msg' + str(i))

    def __init__(self, urls):
        self.urls = urls
        self.files = [os.path.basename(url) for url in urls]

    def connection_made(self, transport):
        print('Connected to Server.')
        self.transport = transport
        loop.call_later(self.TIMEOUT, self.send_from_call_later)

    def data_received(self, data):
        self.data = format(data.decode())
        print('data received: {}'.format(data.decode()))

    def send_from_call_later(self):
        for
        with open()
        self.transport.write(self.msg)
        print('data sent: {}'.format(self.msg))
        print('Removing data: {}'.format(self.event_list[0]))
        del self.event_list[0]
        print(self.event_list)
        print('-----------------------------------------')
        if len(self.event_list) > 0:
            self.client_tcp_timeout = loop.call_later(
                self.TIMEOUT, self.send_from_call_later
            )
        else:
            print('All list was sent to the server.')

    def connection_lost(self, exc):
        print('Connection lost!!!!!!.')

    @staticmethod
    async def download_coroutine(url):
        """
        Сопрограмма для загрузки данных по указанному url
        """
        request = urllib.request.urlopen(url)
        filename = os.path.basename(url)

        with open(filename, 'wb') as file_handle:
            while True:
                chunk = request.read(1024)
                if not chunk:
                    break
                file_handle.write(chunk)
        msg = 'Завершена загрузка {}'.format(filename)
        return msg

    @staticmethod
    async def main(items, coroutine):
        """
        Создет группу сопрограмм и ожидает их завершения
        """
        coroutines = [coroutine(item) for item in items]
        completed, pending = await asyncio.wait(coroutines)
        for item in completed:
            print(item.result())

if __name__ == '__main__':
    urls = ["http://192.168.1.1/1.txt",
            "http://192.168.1.1/2.txt",
            "http://192.168.1.1/3.txt",
            "http://192.168.1.1/4.txt",
            "http://192.168.1.1/5.txt"]

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(urls))
    finally:
        loop.close()
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(Client(urls), 'localhost', 8000)
    client = loop.run_until_complete(coro)
    loop.run_forever()

