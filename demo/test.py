import threading
import time


def worker():
    """thread worker function"""
    time.sleep(1)
    print('Worker')
    return


def worker2():
    """thread worker function"""
    time.sleep(1)
    print('Worker2')
    return


threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    t2 = threading.Thread(target=worker2)
    threads.append(t)
    threads.append(t2)
    t.start()
    t2.start()
    t.join()
    t2.join()
