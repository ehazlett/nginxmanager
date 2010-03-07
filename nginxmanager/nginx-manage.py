#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
#    nginx-manage.py
#        NginxManager control script
#
#    Copyright (C) 2010  Lumentica
#       http://www.lumentica.com
#       info@lumentica.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

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
