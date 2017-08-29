import sys
import threading
import os
from queue import Queue, Empty


def input_enqueued(prompt, q):
    print(prompt, end='', flush=True)
    q.put(sys.stdin.readline().rstrip('\n'))

if __name__ == '__main__':
    q = Queue()
    result = []
    for _ in range(5):
        task = threading.Thread(target=input_enqueued, args=('Input something: ', q), daemon=True)
        task.start()
        try:
            user_input = q.get(timeout=3)
        except Empty:
            user_input = None
        result.append(user_input)
        os.system('cls')
    print(result)
