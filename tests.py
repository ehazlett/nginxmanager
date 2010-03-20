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


