from django.utils import timezone
import time
def FirstCronTest():
    print("")
    print("I am executed..!")

def FirstCronTest2():
    print("")
    start = timezone.now()
    print("I am executed 2..!", start)
    time.sleep(5)
    end = timezone.now()
    print("I am executed 2.. done!", end)