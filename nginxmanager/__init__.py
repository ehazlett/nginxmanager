#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
#    Nginx Manager
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
#

import logging

class NginxConfigParser(object):
    '''Handles parsing Nginx config files'''
    def __init__(self, filename=None):
        self.__filename = filename
        self._log = logging.getLogger('NginxConfigParser')

    def parse_global(self):
        '''Parses the 'global' nginx options'''
        self._log.debug('Parsing global section...')
        f = open(self.__filename, 'r')
        cfg = f.read()
        f.close()
        options = {}
        # loop through and gather options
        in_section = False
        for l in cfg.split('\n'):
            # skip commented sections and blank lines
            if not l.strip().startswith('#'):
                if l.strip() != '':
                    # parse options
                    if l.find('{') == -1 and not in_section:
                        # check for final semi-colon
                        if l.find('}') == -1:
                            # remove semi-colons and parse
                            op = l.replace(';','').split(None, 3)
                            options[op[0]] = op[1:]
                    # found 'start' section tag; mark and ignore contents
                    elif l.find('{') > -1:
                        in_section = True
                    # found 'end' section marker
                    elif l.find('}') > -1:
                        in_section = False
        return options
    
    def parse_http(self):
        '''Parses 'http' section'''
        self._log.debug('Parsing http section...')
        f = open(self.__filename, 'r')
        cfg = f.read()
        f.close()
        options = {}
        # loop through and gather options
        in_http_section = False
        in_section = False
        subsection_count = 0
        for l in cfg.split('\n'):
            # skip commented sections and blank lines
            if not l.strip().startswith('#'):
                if l.strip() != '':
                    # parse options
                    if l.find('{') > -1 and l.find('http') > -1 and not in_section:
                        in_http_section = True
                    elif l.find('{') == -1 and in_http_section and subsection_count == 0:
                        # check for final semi-colon
                        if l.find('}') == -1:
                            # remove semi-colons and parse
                            op = l.replace(';','').split(None, 3)
                            options[op[0]] = op[1:]
                        else:
                            in_http_section = False
                    # found 'start' section tag; mark and ignore contents
                    elif l.find('{') > -1:
                        subsection_count += 1
                    # found 'end' section marker
                    elif l.find('}') > -1:
                        subsection_count -= 1
        return options


class NginxConfig(object):
    ''' 
        Manages Nginx configurations
    '''
    def __init__(self, filename=None):
        self._log = logging.getLogger('NginxConfig')
        if not filename:
            self._log.error('You must specify a config filename...')
            return
        self.__filename = filename
        self.__global = {}
        self.__http = {}
        self.__servers = {}
        self.__parser = NginxConfigParser(self.__filename)
    
    # accessors
    def get_filename(self): return self.__filename
    def get_global(self): return self.__global
    def get_http(self): return self.__http

    def _load_global(self):
        self.__global = self.__parser.parse_global()

    
