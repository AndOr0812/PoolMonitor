# -*- coding: utf-8 -*-
__author__ = 'dk'

import time
import threading
import thread
import traceback
import sys


class Smartworker(threading.Thread):


    def __init__(self, threadname, func, args):

        self.func = func
        self.param = args
        self.threadname = threadname
        threading.Thread.__init__(self)


    def run(self):
        strs = ""
        num = len(self.param)

        for i in range(0,num):
            strs += "self.param[%d]" % i
            if i == num -1:
                pass # do nothing
            else:
                strs += ","
        try:
            eval("self.func(%s)" % strs)
        except:

            print "thread_erro:"+str(sys.exc_info())
            print "thread_erro:"+traceback.format_exc()


def addtosubthread(threadname, func, *args):

    worker = Smartworker(threadname, func, args)

    if worker ==None:
        return False
    worker.setDaemon(True)
    while True:
        try:
            worker.start()
        except thread.error:
            print str(sys.exc_info())
            print traceback.format_exc()
            time.sleep(5)
        else:
            break
