# Example of threads with different functions

import threading
import time

class Hello(threading.Thread):
    def run(self):
        print("started 1")
        time.sleep(2)
        print("hello")

class Hi(threading.Thread):
    def run(self):
        time.sleep(2)
        print("started 2")
        print("hi there")

threads = [Hello(), Hi()]
for thread in threads:
    thread.start()
