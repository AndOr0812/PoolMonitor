# -*- coding:utf-8 -*-
__author__ = 'dk'

import subprocess
import os
import os.path
import time
import re

import msg_option
import global_param
import new_subthread
import signal_option

'''
    loop the log file dict ,tail -f every logfile,
    every thread loop for the log,dispatch and get the signal for new block.
'''

class PoolMonitor(object):

    log_dir = global_param.log_dir
    block_sed = "Stratum from pool 0 detected new block"
    regex = re.compile(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})')

    @classmethod
    def get_cmd(cls, pool_name):
        abs_file_name = "%s/%s.log" % (cls.log_dir, pool_name)
        if os.path.exists(abs_file_name):
            return "tail -f -n -500 %s" % abs_file_name
        return ""


    @classmethod
    def mag_handler(cls, re_params):
        msg = re_params.get("msg")
        if msg:
            # p = re.compile(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})')
            m = cls.regex.search(msg)
            #  m = p.search(r'[2015-05-11 17:01:32] Accepted 015ed4c4 Diff 187/128 AMU 0')
            cur_time = m.group(0)
            del re_params["msg"]
            re_params["cur_time"] = cur_time
            global_param.lock_dict["msg_list_lock"].acquire()
            global_param.msg_list.append(re_params)
            global_param.lock_dict["msg_list_lock"].release()


    @classmethod
    def depatch(cls, pool_name="", logname=""):
        cmd = cls.get_cmd(logname)
        if not cmd:
            print "%s dir log file %s.log not exit" % (cls.log_dir, pool_name)
            return False
        global_param.log.warning("cmd: %s" % cmd)
        # print "cmd: %s" % cmd
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while True:
            line = popen.stdout.readline().strip()
            # 判断内容是否为空

            if line and cls.block_sed in line.strip():
                # print line
                if pool_name == "AntPool.1":
                    pool_name = "AntPool"
                re_params = {"pool_name": pool_name}
                re_params["msg"] = line.strip()
                pre_value = line.split("%s," % cls.block_sed)[1].strip()
                re_params["Hash"] = pre_value.split(",")[0].strip()
                re_params["time_sed"] = pre_value.split(",")[1].strip()

                cls.mag_handler(re_params)

                # new_subthread.addtosubthread("new_block_%s" % re_params["uuid"], Msg_sender.dispatch, re_params)




def Pool_monitor_option():

    for key, value in global_param.log_dict.items():
        new_subthread.addtosubthread("%s_new_block" % key, PoolMonitor.depatch, key, value)
    new_subthread.addtosubthread("msg_sender", msg_option.msg_option)
    new_subthread.addtosubthread("signal_sender", signal_option.Signal_Sender.monit_loop)

    while True:
        time.sleep(5)


if __name__ == "__main__":
    Pool_monitor_option()