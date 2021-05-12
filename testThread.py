import _thread
import time


def print_line(delay):
    lists = list(range(100))
    for i in lists:
        time.sleep(delay)
        print("现在的进度1是%d"%i+"%")

def print_line2(delay):
    lists = list(range(100))
    for i in lists:
        time.sleep(delay)
        print("现在的进度2是%d"%i+"%")

try:
    _thread.start_new_thread(print_line,(1,))
    _thread.start_new_thread(print_line2,(2,))
except:
    print("error")
