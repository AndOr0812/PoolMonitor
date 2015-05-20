# -*- coding:utf-8 -*-
import threading
__author__ = 'dk'

log_dir = "/home/kevin/Desktop/"

log_dict = {
    "AntPool": "antpool",
    "F2Pool": "f2pool",
    "BW.COM": "BW_COM",
    "BTCChina Pool": "BTCChina_Pool",
    "BitFury": "",
    "KnCMiner": "",

}

# target_url = "http://10.0.222.121:8000/show/api/v1/record"
# end_url = "http://10.0.222.121:8000/show/api/v1/confirm"
target_url = "http://10.12.70.236:8000/show/api/v1/record"
end_url = "http://10.12.70.236:8000/show/api/v1/confirm"
last_list = []

# {"hash_value":"time_sed"}
hash_dict = {}
lock_dict = {
 "last_list_lock": threading.Lock(),
 "hash_dict": threading.Lock(),
}
