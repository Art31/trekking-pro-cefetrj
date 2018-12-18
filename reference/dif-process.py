# Example of processes with different functions

from multiprocessing import Process
import time

def Hello():
    print("start hello")
    time.sleep(5)
    print("hello")

def Hi():
    print("start hi")
    time.sleep(5)
    print("hi there")

hello = Process(target=Hello)
hi = Process(target=Hi)

threads = [hello, hi]
for thread in threads:
    thread.start()
