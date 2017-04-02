
import socket
import keyboard

__author__ = 'Наумов Александр Сергеевич'


def find_port(server, port_range, response):
    for port in port_range:
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.settimeout(0.001)
        try:
            _socket.connect((server, port))
            _socket.send(bytes('Test connection', 'utf-8'))
            _response = _socket.recv(1024)
        except (socket.timeout, OSError):
            _socket.close()
        else:
            if str(_response, 'utf-8') == response:
                return port


def fill_buffer(event):
    if len(buffer) < 10:
        buffer.append(event.name)
    else:
        keyboard.unhook(fill_buffer)
        keyboard.hook(keyboard_event)


def keyboard_event(event):
    if not buffer and event.name == 's':
        keyboard.unhook(keyboard_event)
        keyboard.hook(fill_buffer)
    elif event.name == 'esc':
        buffer[0] = False


HOST = 'localhost'
# PORT = 9999
print('Try to connect to server')
PORT = find_port(HOST, range(9000, 10000), 'Connection is OK')
if PORT:
    buffer = []
    response = []
    keyboard.hook(keyboard_event)

    while (not buffer or buffer[0]) and len(buffer) < 10:
        pass
    if buffer[0]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print('Клиент запущен')
        sock.send(bytes(' '.join(buffer), 'utf-8'))
        response.append(str(sock.recv(1024), 'utf-8'))

        print(response)

        sock.close()
else:
    print('Can not connect to {}'.format(HOST))
