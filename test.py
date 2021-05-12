import _thread
import datetime
import glob
import time
import unittest
from time import sleep

import cv2
from cv2 import VideoCapture, VideoWriter


class TestSkadi(unittest.TestCase):

    def test_format(self):
        size = (5306, 4045)
        print(size)
        videowrite = cv2.VideoWriter(r'F:\test.mp4', -1, 60, size)
        img_array = []
        for filename in [r'F:\interact\skadi l2d idle_00{0}.png'.format(i) for i in range(10)]:
            img = cv2.imread(filename)
            if img is None:
                print(filename + " is error!")
                continue
            img_array.append(img)
        for i in range(10):
            videowrite.write(img_array[i])
        print('end!')

    def test_uu(self):
        str = ""
        for i in range(105):
            if i < 10:
                str = "F:\hu\skadi00{0}".format(i)
            elif i < 100 and i >= 10:
                str = "F:\hu\skadi0{0}".format(i)
            elif i < 105 and i >= 100:
                str = "F:\hu\skadi{0}".format(i)
            print(str)

    def test_pr(self):
        # 为线程定义一个函数
        def print_time(threadName, delay):
            count = 0
            while count < 5:
                time.sleep(delay)
                count += 1
                print("%s: %s" % (threadName, time.ctime(time.time())))

        def print_time2(threadName, delay):
            count = 0
            while count < 5:
                time.sleep(delay)
                count += 1
                print("%s: %s" % (threadName, time.ctime(time.time())))
        # 创建两个线程
        try:
            _thread.start_new_thread(print_time, ("Thread-1", 2,))
            _thread.start_new_thread(print_time2, ("Thread-2", 4,))
        except:
            print("Error: 无法启动线程")

        while 1:
            pass
