#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
#    tests.py   
#        Tests for NginxManager
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


import unittest
import os
import stat
import sys
# set path
sys.path.append(os.path.dirname(os.getcwd()))    
#import settings
import logging
import tempfile
import shutil
from optparse import OptionParser
from nginxmanager import NginxConfigParser

class TestNginxConfigParser(unittest.TestCase):
    def setUp(self):
        self.filename = os.path.join('test', 'nginx.conf.default')
        self.nginx_parser = NginxConfigParser(self.filename)
        self.log = logging.getLogger('TestNginxConfigParser')

    def testParseGlobal(self):
        opts = self.nginx_parser.parse_global()
        self.assertTrue(opts.has_key('user'))
        self.assertTrue(opts.has_key('worker_processes'))
        self.assertTrue(not opts.has_key('error_log'))
        self.assertTrue(opts.has_key('pid'))
    
    def testParseSection(self):
        opts = self.nginx_parser.parse_section('http')

if __name__ == '__main__':
    LOG_LEVEL=logging.ERROR
    LOG_FILE='tests.log'
    LOG_CONFIG=logging.basicConfig(level=LOG_LEVEL,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d-%Y %H:%M:%S',
        filename=LOG_FILE,
        filemode='w')
        
    # run tests
    unittest.main()


