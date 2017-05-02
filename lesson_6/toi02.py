import time
import asyncio
import threading
import sys


def stop_loop(timeout, loop):
    time.sleep(timeout)
    loop.call_soon_threadsafe(loop.stop)


loop = asyncio.get_event_loop()
threading.Thread(target=stop_loop, args=(3, loop)).start()
print('Input something: ', end='', flush=True)
loop.run_until_complete(sys.stdin.readline())
loop.close()  # optional