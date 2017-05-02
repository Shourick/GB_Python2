import _thread
import threading


# def raw_input_with_timeout(prompt, timeout=30.0):
#     print(prompt)
#     timer = threading.Timer(timeout, _thread.interrupt_main)
#     astring = None
#     try:
#         timer.start()
#         astring = input(prompt)
#     except KeyboardInterrupt:
#         pass
#     timer.cancel()
#     return astring

import msvcrt
import time


def raw_input_with_timeout(prompt, timeout=30.0):
    print(prompt)
    finishat = time.time() + timeout
    result = []
    while True:
        if msvcrt.kbhit():
            result.append(msvcrt.getwche())
            print(result)
            if result[-1] == '\n':   # or \n, whatever Win returns;-)
                return ''.join(result)
        else:
            if time.time() > finishat:
                return None
        time.sleep(0.1)          # just to yield to other processes/threads

if __name__ == '__main__':
    answer = raw_input_with_timeout('Are you sure? Yes/No: ', 3)
    print(answer)
