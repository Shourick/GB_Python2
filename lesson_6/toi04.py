import asyncio
import sys
from time import time


def process_input():
    text = sys.stdin.readline()
    n = text.strip()
    print('User input is {}'.format(n))


async def print_hello():
    while True:
        # print("{} - Hello world!".format(int(time())))
        await asyncio.sleep(3)


def main():
    loop = asyncio.get_event_loop()
    loop.add_reader(sys.stdin, process_input)
    loop.run_until_complete(print_hello())


if __name__ == '__main__':
    main()
