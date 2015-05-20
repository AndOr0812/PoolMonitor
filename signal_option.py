# -*- coding:utf-8 -*-
__author__ = 'dk'
import time
import global_param
import urllib
import urllib2
import sys,traceback

class Signal_Sender(object):


    @classmethod
    def send_signal(cls, hash_value):
        if hash_value:
            msg = {"Hash_value": hash_value}
            url = global_param.end_url
            body = urllib.urlencode(msg)
            res_context = ""
            try:

                res_context = urllib2.urlopen(url, body).read()
                print "target_url: %s res_context: %s hash_value : %s" % (url, res_context, body)

            except Exception, err:
                print(traceback.format_exc())
                print(sys.exc_info()[0])
            finally:
                return res_context


    @classmethod
    def change_signal(cls):
        global_param.lock_dict["hash_dict"].acquire()
        if global_param.hash_dict:

            for key, value in global_param.hash_dict.items():
                time.sleep(2)
                if float(value) < time.time() - 30:
                    if cls.send_signal(key):
                        del global_param.hash_dict[key]
            print "now hash_dict: %s " % global_param.hash_dict
        global_param.lock_dict["hash_dict"].release()


    @classmethod
    def monit_loop(cls):

        while True:
            time.sleep(10)
            print "start send signal"
            cls.change_signal()
            time.sleep(20)


if __name__ == "__main__":
    Signal_Sender.monit_loop()
