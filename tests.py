#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
#    tests.py   
#        Tests for NginxManager
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
        self.filename = os.path.join('test', 'nginx.conf')
        self.nginx_parser = NginxConfigParser(self.filename)
        self.log = logging.getLogger('TestNginxConfigParser')

    def testParseGlobal(self):
        opts = self.nginx_parser.get_global()
        self.assertTrue(opts.has_key('user'))
        self.assertTrue(opts.has_key('worker_processes'))
        self.assertTrue(not opts.has_key('error_log'))
        self.assertTrue(opts.has_key('pid'))

    def testParseHttp(self):
        opts = self.nginx_parser.get_http()
        self.assertTrue(opts.has_key('sendfile'))
        self.assertTrue(opts.has_key('include'))
        self.assertTrue(not opts.has_key('location'))
    
    def testParseServers(self):
        opts = self.nginx_parser.get_servers()
        for s in opts:
            self.assertTrue(s.has_key('locations'))
            [self.assertTrue(x.has_key('options')) for x in s['locations']]
    
    def testParseUpstreams(self):
        opts = self.nginx_parser.get_upstreams()
        for u in opts:
            self.assertTrue(u.has_key('name'))
            self.assertTrue(u.has_key('options'))

if __name__ == '__main__':
    # run tests
    unittest.main()


