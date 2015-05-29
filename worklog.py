#-*-coding:utf-8-*-
import logging

def logconf(logname,logger):

    # 创建一个logger
    logcreater = logging.getLogger(logger)
    logcreater.setLevel(logging.DEBUG)
    
    fh = logging.FileHandler(logname)
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s  %(name)s : %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logcreater.addHandler(fh)
    logcreater.addHandler(ch)
    return logcreater