
# Сервер платёжного терминала

import socketserver

__author__ = 'Наумов Александр Сергеевич'


class MemTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).decode('utf-8')
        print("Клиент {} сообщает {}".format(self.client_address[0], self.data))

        if self.data == 'Test connection':
            self.request.send(bytes('Connection is OK', 'utf-8'))
        elif self.data.startswith('s'):
            self.request.send(
                bytes('{} was received'.format(self.data), 'utf-8')
            )
        else:
            print('Неизвестный запрос')    

          
HOST, PORT = 'localhost', 9999

server = socketserver.TCPServer((HOST, PORT), MemTCPHandler)  
print('Testing server is running')

server.serve_forever()

