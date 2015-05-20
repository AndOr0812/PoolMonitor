# -*- coding:utf-8 -*-
__author__ = 'dk'

import re
import urllib
import urllib2
import sys,traceback

import global_param



class Msg_sender(object):

    regex = re.compile(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})')
    target_url = global_param.target_url

    @classmethod
    def send_last(cls):

        if global_param.last_list:
            global_param.lock_dict["last_list_lock"].acquire()
            for idx, item in enumerate(global_param.last_list):
                global_param.last_list.pop(idx)
                if cls.send_msg(item):
                    cls.add_hash(item)
                else:
                    global_param.last_list.append(item)
            global_param.lock_dict["last_list_lock"].release()


    @classmethod
    def dispatch(cls, send_msg):
        pre_frame = cls.mag_handler(send_msg)

        cls.send_last()
        if cls.send_msg(pre_frame):
            cls.add_hash(pre_frame)
        else:
            global_param.last_list.append(pre_frame)


    @classmethod
    def add_hash(cls, msg):
        global_param.lock_dict["hash_dict"].acquire()
        global_param.hash_dict[msg.get("Hash")] = msg.get("time_sed")
        global_param.lock_dict["hash_dict"].release()



    @classmethod
    def send_msg(cls, msg):
        # print "msg: %s" % str(msg)
        # frame = zlib.compress(str(msg), 9)
        body = urllib.urlencode(msg)
        # print "body: %s" % body
        res_context = ""
        try:
            print "target_url: %s res_context: %s  body: %s " % (cls.target_url, res_context, str(msg))
            #resp, res_context = h.request(cls.target_url, "POST", body)
            #print resp
            # res_context = res_context = urllib2.urlopen(cls.target_url, body, 5).read()

            res_context = urllib2.urlopen(cls.target_url, body).read()
            print "target_url: %s res_context: %s" % (cls.target_url, res_context)
        except Exception, err:
            print(traceback.format_exc())
            print(sys.exc_info()[0])

        finally:
            return res_context


    @classmethod
    def mag_handler(cls, re_params):
        msg = re_params.get("msg")
        if msg:
            # p = re.compile(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})')
            m = cls.regex.search(msg)
            #  m = p.search(r'[2015-05-11 17:01:32] Accepted 015ed4c4 Diff 187/128 AMU 0')
            cur_time = m.group(0)
            del re_params["msg"]
            del re_params["uuid"]
            re_params["cur_time"] = cur_time

        return re_params