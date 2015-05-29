# -*- coding:utf-8 -*-
__author__ = 'dk'


import threading
import worklog


log_dir = "/var/log/cgminer/"

log_dict = {
    "AntPool": "antpool",
    "F2Pool": "f2pool",
    "BW.COM": "BW_COM",
    "BTCChina Pool": "BTCChina_Pool",
    "Slush": "Slush",
    "AntPool.1": "antpool.1",


}

# target_url = "http://10.0.222.121:8000/show/api/v1/record"
# end_url = "http://10.0.222.121:8000/show/api/v1/confirm"
target_url = "http://10.0.222.123/show/api/v1/record"
end_url = "http://10.0.222.123/show/api/v1/confirm"
msg_list = []

# {"hash_value":"time_sed"}
hash_dict = {}
lock_dict = {
    "hash_dict": threading.Lock(),
    "msg_list_lock": threading.Lock(),
}

log = worklog.logconf("/var/log/monitor.log", "PoolMonitor")
