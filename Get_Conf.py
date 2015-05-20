# -*- coding:utf-8 -*-
__author__ = 'dk'

import os
import subprocess


class Proj_Conf(object):

    def __init__(self):
        self.usb_list = []
        self.cmd_sed = "cd /home/kevin/Desktop/cgminer-4.8.0 && nohup ./cgminer --bmsc-options 115200:1 "
        self.cmd_dict = {
            "AntPool": "",
            "F2Pool": "",
            "BW.COM": "",
            "BTCChina Pool": "",
            "BitFury": "",
            "KnCMiner": "",
        }
        self.pool_conf = {
            "AntPool": {"user": "-u ZHANGWENHUI.1", "url": "-o solo.antpool.com:3333", "usb_id": "--usb ", "log": "--logfile /home/kevin/Desktop/antpool.log" ,"enable": False},
            "F2Pool": {"user": "-u antforzhw.1", "url": "-o stratum.f2pool.com:3333", "usb_id": "--usb ", "log": "--logfile /home/kevin/Desktop/f2pool.log","enable": False},
            "BW.COM": {"user": "-u antminer.1", "url": "-o stratum+tcp://stratum_0310.bw.com:3333", "usb_id": "--usb ", "log": "--logfile /home/kevin/Desktop/BW_COM.log", "enable": False},
            "BTCChina Pool": {"user": "-u antforzhw.1 -p sishen2008", "url": "-o stratum+tcp://stratum.btcchina.com:3333", "usb_id": "--usb ", "log": "--logfile /home/kevin/Desktop/BTCChina_Pool.log", "enable": False},
            "BitFury": {},
            "KnCMiner": {},
        }

    def conf_option(self):

        self.get_usb_id()
        print self.usb_list
        self.set_pool_conf()
        self.init_cmd_dict()

    def get_usb_id(self):

        cmd = ''' lsusb | grep "myAVR mySmartUSB light" | grep -v grep |awk  '{print $2 $4}' '''

        res_lines = os.popen(cmd).readlines()
        for line in res_lines:

            line_data = line.strip()
            usb_id = "%s:%s" % (line_data[:3], line_data[3:6])
            self.usb_list.append(usb_id)

    def set_pool_conf(self):

        for key, value in self.pool_conf.items():
            if self.usb_list and value:
                usb_id = self.usb_list.pop()
                value["usb_id"] = "--usb %s" % usb_id
                value["enable"] = True
        print " self.usb_list : %s " % self.usb_list

    def init_cmd_dict(self):

        for pool_name, conf in self.pool_conf.items():

            if conf.get("enable"):
                pool_cmd = "%s %s %s %s %s &" % (self.cmd_sed, conf.get("user", ""), conf.get("url", ""), conf.get("usb_id", ""), conf.get("log", ""))
                self.cmd_dict[pool_name] = pool_cmd
        print "after init cmd dict, self.cmd_dit : %s" % str(self.cmd_dict)


    def run_cgminer(self):

        for item in self.cmd_dict.values():
            if item:
                os.system(item)



if __name__ == "__main__":

    procj_creater = Proj_Conf()

    procj_creater.conf_option()
    procj_creater.run_cgminer()



