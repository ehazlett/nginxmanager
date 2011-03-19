#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
#    nginx-manage.py
#        NginxManager control script
#
#    Copyright (C) 2011  Lumentica
#       http://www.lumentica.com
#       info@lumentica.com
#
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import sys
# add current directory to python path
sys.path.insert(0, os.path.dirname(os.getcwd()))
import logging
from optparse import OptionParser


VERSION = '0.1'

# logging vars
LOG_LEVEL = logging.DEBUG
# set to debug for testing
LOG_FILE='nginx-manager.log'

def setup_logging():
    LOG_CONFIG=logging.basicConfig(level=LOG_LEVEL, # always log debug to file
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d-%Y %H:%M:%S',
                        filename=LOG_FILE,
                        filemode='a')
                    
    logging.config=LOG_CONFIG
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console.setFormatter(formatter)
    console.setLevel(LOG_LEVEL)
    logging.getLogger('').addHandler(console)
log = logging.getLogger('NginxManager')

if __name__ == '__main__':
    # options
    op = OptionParser()
    op.add_option('-d', '--debug', dest='debug', action="store_true", default=False, help='Show debug')
    opts, args = op.parse_args()
    
    setup_logging()
    from nginxmanager import NginxConfigParser
    ng = NginxConfigParser('../test/nginx.conf.default')
