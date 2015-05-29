# -*- coding:utf-8 -*-
__author__ = 'dk'

import urllib
import urllib2
import sys,traceback
import time

import global_param



class Msg_sender(object):


    target_url = global_param.target_url



    @classmethod
    def dispatch(cls, send_msg):

        res_msg = cls.send_msg(send_msg)
        if res_msg :
            if res_msg == "ok":
                cls.add_hash(send_msg)
        else:
            global_param.lock_dict["msg_list_lock"].acquire()
            global_param.msg_list.insert(0, send_msg)
            global_param.lock_dict["msg_list_lock"].release()


    @classmethod
    def add_hash(cls, msg):
        global_param.lock_dict["hash_dict"].acquire()
        global_param.hash_dict[msg.get("Hash")] = msg.get("time_sed")
        global_param.lock_dict["hash_dict"].release()



    @classmethod
    def send_msg(cls, msg):

        body = urllib.urlencode(msg)
        res_context = ""
        try:
            res_context = urllib2.urlopen(cls.target_url, body).read()
            global_param.log.warning("target_url: %s res_context: %s  body: %s " % (cls.target_url, res_context, str(msg)))

        except Exception, err:
            global_param.log.error(traceback.format_exc())
            global_param.log.error(sys.exc_info()[0])
            print(traceback.format_exc())
            print(sys.exc_info()[0])

        finally:
            return res_context


def msg_option():
    time.sleep(4)
    while 1:
        global_param.lock_dict["msg_list_lock"].acquire()
        pre_frame = ""
        if global_param.msg_list:
            pre_frame = global_param.msg_list.pop()
        global_param.lock_dict["msg_list_lock"].release()
        if pre_frame:
            Msg_sender.dispatch(pre_frame)
        time.sleep(0.01)
