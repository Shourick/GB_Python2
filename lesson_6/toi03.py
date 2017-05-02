import sys
import time
import threading
import os


def input_with_timeout(prompt, q):
    mutex.acqurie()
    print(prompt, end='', flush=True)
    q[0] = sys.stdin.readline().rstrip('\n')
    print(q[0], flush=True)

user_input = [None]
result = []
mutex = threading.Lock()
for _ in range(15):
    user_input = [None]
    task_input = threading.Thread(target=input_with_timeout, args=('Input something: ', user_input), daemon=True)
    task_input.start()
    mutex.release()
    time.sleep(2)
    result.append(user_input[0])
    # print('\nYour answer is: {}'.format(str(user_input[0])))
    if task_input.is_alive():
        task_input._reset_internal_locks(False)
        task_input._stop()
        time.sleep(0.2)
        # task_input.join()
    os.system('cls')
print(result)