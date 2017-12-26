#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/25 下午5:30
# @Author  : zpy
# @Software: PyCharm

import logging
import logging.config
from logging.handlers import SocketHandler, RotatingFileHandler

FORMAT = "%(asctime)-15s %(threadName)s %(filename)s:%(lineno)d %(levelname)s %(message)s"

logging.basicConfig(level=logging.DEBUG, format=FORMAT)

logger = logging.getLogger('newframe')
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

if __name__ == '__main__':
    logger.debug("wtf")
    logger.info('wtff')