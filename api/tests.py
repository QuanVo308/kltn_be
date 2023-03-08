from threading import Thread
import math
import os

class PropagatingThread(Thread):
    def run(self):
        self.exc = None
        try:
            if hasattr(self, '_Thread__target'):
                # Thread uses name mangling prior to Python 3.
                self.ret = self._Thread__target(
                    *self._Thread__args, **self._Thread__kwargs)
            else:
                self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self.exc = e


def test(a):
    print(a)

def multithread(thread):
    threads = []
    for thread_num in range(0, 5):
        threads.append(PropagatingThread(
            target=test, args=(f"{thread} {thread_num}",)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

threads = []
for thread_num in range(0, 5):
    threads.append(PropagatingThread(
        target=multithread, args=(thread_num,)))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(round(math.log(4 * 1.5,2)))
