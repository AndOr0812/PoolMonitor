# -*- coding:utf-8 -*-
__author__ = 'dk'

import os

class Mutil_Thread(object):

    def __init__(self):
        self.cmd_list = []

    def make_cmd(self):
        port_list = [8000, 8001, 8002, 8003, 8004, 8005]
        cmd_sed = "cd &python manage.py runserver 0.0.0.0:"

        for item in port_list:
            self.cmd_list.append("%s%s" % (cmd_sed, str(item)))

        print "cmd_list : %s" % str(self.cmd_list)

    def run_server(self):

        for item in self.cmd_list:

            os.system(item)


if __name__ == "__main__":

    mu_obj = Mutil_Thread()
    mu_obj.make_cmd()
    mu_obj.run_server()




