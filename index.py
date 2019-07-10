#!/usr/bin/python3

import threading
import datetime

class StartClass():
    def __init__(self):
        print('init')

    def test(self):
        print('TimeNow:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        # t.start()


def test2():
    print('hello22')


if __name__ == '__main__':
    sc = StartClass()
    t = threading.Timer(5, test2())
    t.start()
    # sc.test()

