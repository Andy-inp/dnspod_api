#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import logging
import logging.config
import logging.handlers
import sys, os
Base_Dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Custom Logger 
logging.config.fileConfig(f"{Base_Dir}/conf/mylogging.conf")
mylogger = logging.getLogger('mylogger')
