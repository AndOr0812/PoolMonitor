# -*- coding:utf-8 -*-
__author__ = 'dk'
import ConfigParser
import os


class ConfigReader(object):

    def __init__(self):
        self.conf_path = "/root/proj_path/PoolMonitor/conf.ini"

    def get_conf(self):
        conf_dict = {}
        config = ConfigParser.ConfigParser()
        config.read(self.conf_path)
        # kvs = config.items("info")
        # print 'sec_a:', kvs
        conf_dict["username"] = config.get("info", "username")
        conf_dict["passward"] = config.get("info", "passward")
        conf_dict["pool_url"] = config.get("info", "pool_url")
        conf_dict["log_path"] = config.get("info", "log_path")
        conf_dict["name_start"] = config.get("info", "name_start")
        conf_dict["name_end"] = config.get("info", "name_end")
        conf_dict["pool_name"] = config.get("info", "pool_name")

        print "conf_dict :　%s" % str(conf_dict)

        return conf_dict








class Proj_Conf(object):

    def __init__(self, params):
        self.usb_list = []
        self.cmd_list = []
        self.username = params.get("username")
        self.passward = params.get("passward", "")
        self.pool_url = params.get("pool_url")
        self.log_path = params.get("log_path", "/var/log/")
        self.name_start = int(params.get("name_start", "1"))
        self.name_end = int(params.get("name_end", "10"))
        self.pool_name = params.get("pool_name", "antpool")
        self.cmd_sed = "cd /root/proj_path/cgminer-4.8.0 && nohup ./cgminer --bmsc-options 115200:1 "




    def get_usb_id(self):

        cmd = ''' lsusb | grep "myAVR mySmartUSB light" | grep -v grep |awk  '{print $2 $4}' '''

        res_lines = os.popen(cmd).readlines()
        for line in res_lines:

            line_data = line.strip()
            usb_id = "%s:%s" % (line_data[:3], line_data[3:6])
            self.usb_list.append(usb_id)

    def init_cmd(self, user_id, usb_id):
        antminer = "%s.%s" %(self.username, str(user_id))
        user_info = "-u %s " % antminer
        if self.passward and "antpool" not in self.pool_url:
            user_info = "-u  %s -p %s " % (antminer, self.passward)

        pool_info = "-o %s " % self.pool_url
        log_file = "--logfile %s " % os.path.join(self.log_path, "%s.%s.log" % (str(user_id), self.pool_name))
        usb_info = "--usb %s " % usb_id

        pool_cmd = "%s %s %s %s %s >/dev/null 2>error_log &" % (self.cmd_sed, user_info, pool_info, usb_info, log_file)

        return pool_cmd


    def make_cmd_list(self):
        self.get_usb_id()

        usb_num = len(self.usb_list)
        if usb_num < (self.name_end - self.name_start):
            for index in range(self.name_start, self.name_start+usb_num):
                usb_id = self.usb_list[index-self.name_start]
                print "usb_id %s user_Id %s" % (index, usb_id)
                pool_cmd = self.init_cmd(index, usb_id)
                if pool_cmd:
                    self.cmd_list.append(pool_cmd)

        print "cmd list : %s" % str(self.cmd_list)


    def run_cgminer(self):

        for item in self.cmd_list:
            if item:
                os.system(item)









if __name__ == "__main__":
    confreader = ConfigReader()
    conf_dict = confreader.get_conf()
    proj_conf = Proj_Conf(conf_dict)
    proj_conf.make_cmd_list()
    proj_conf.run_cgminer()



