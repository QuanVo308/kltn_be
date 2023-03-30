
from threading import Thread
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

def test(num, list_num):
    # print(num)
    for i in range(num):
        list_num.append({'test':i})

all_list = {}

threads = []
for i in range(4):
    temp_list = []
    all_list[f'{i}'] = temp_list
    threads.append(PropagatingThread(
                    target=test, args=(i, temp_list,)))

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

all_l = []
for key in all_list:
    print(key)
    all_l.extend(all_list[key])

all_l = sorted(all_l, key=lambda d: d['test'], reverse=True)
print(all_list)
print(all_l)
