#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
#    Nginx Manager
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

import logging
import os

class NginxConfigParser(object):
    '''Handles parsing Nginx config files'''
    def __init__(self, filename=None):
        self.__filename = filename
        self._log = logging.getLogger('NginxConfigParser')

    def get_global(self):
        """
        Gets the 'global' nginx options

        returns: Dict of option names with values

        """
        self._log.debug('Parsing global section')
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
                            op = l.replace(';','').split(None, 1)
                            options[op[0]] = op[1:]
                            self._log.debug('Added option: %s: %s' % (op[0], op[1:]))
                    # found 'start' section tag; mark and ignore contents
                    elif l.find('{') > -1:
                        in_section = True
                    # found 'end' section marker
                    elif l.find('}') > -1:
                        in_section = False
        return options
    
    def get_http(self):
        """
        Gets 'http' section
        
        returns: Dict of option names with values

        """
        self._log.debug('Parsing http section')
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
                        self._log.debug('Found http section')
                    elif l.find('{') == -1 and in_http_section and subsection_count == 0:
                        # check for final semi-colon
                        if l.find('}') == -1:
                            # remove semi-colons and parse
                            op = l.replace(';','').split(None, 1)
                            options[op[0]] = op[1:]
                            self._log.debug('Added option: %s: %s' % (op[0], op[1:]))
                        else:
                            in_http_section = False
                    # found 'start' section tag; mark and ignore contents
                    elif l.find('{') > -1:
                        subsection_count += 1
                    # found 'end' section marker
                    elif l.find('}') > -1:
                        subsection_count -= 1
        return options

    def get_servers(self):
        """
        Gets all 'server' sections
        
        returns: Dict containing options with values as well as Dict with location options and values.

        Example: 
        
        s = get_servers()
        
        To get the first server's 'server_name' key:

        >>> s[0]['server_name']  
        ['localhost']

        To get first server's 'location' entries:
        >>> s[0]['locations']
        [{'name': '/', 'options': {'root': ['html']}}, {'name': '/50x.html', 'options': {'root': ['html']}}]

        """
        self._log.debug('Parsing server sections...')
        f = open(self.__filename, 'r')
        cfg = f.read()
        f.close()
        # list for all 'server' sections found
        servers = []
        # list for all 'location' sections found in current 'server' section
        locations = []
        # options for 'server' section
        server = {}
        # current 'location' options
        location = {}
        location_options = {}
        # loop through and gather options
        in_server_section = False
        in_section = False
        subsection_count = 0
        for l in cfg.split('\n'):
            # skip commented sections and blank lines
            if not l.strip().startswith('#'):
                if l.strip() != '':
                    # parse options
                    if l.find('{') > -1 and l.find('server') > -1 and not in_section:
                        in_server_section = True
                        self._log.debug('Found server section')
                    elif l.find('{') == -1 and in_server_section and not in_section:
                        # check for final semi-colon
                        if l.find('}') == -1:
                            # remove semi-colons and parse
                            op = l.replace(';','').split(None, 1)
                            server[op[0]] = op[1:]
                            self._log.debug('Added option: %s: %s' % (op[0], op[1:]))
                        else:
                            in_server_section = False
                            server['locations'] = locations
                            servers.append(server)
                            server = {}
                            locations = []
                            location_options = {}
                    # found 'start' section tag; mark and ignore contents
                    elif l.find('{') > -1 and l.find('location') > -1:
                        in_section = True
                        if l.find('location =') > -1:
                            location_name = l.split('location =')[-1].replace('{', '').strip()
                        elif l.find('location '):
                            location_name = l.split(None, 1)[-1].replace('{', '').strip()
                        location['name'] = location_name
                        self._log.debug('Found location section: %s' % (location['name']))
                    # parse 'location' options
                    elif l.find('{') == -1 and in_server_section and in_section:
                        # check for final semi-colon
                        if l.find('}') == -1:
                            # remove semi-colons and parse
                            op = l.replace(';','').split(None, 1)
                            location_options[op[0]] = op[1:]
                            self._log.debug('Added location option: %s: %s' % (op[0], op[1:]))
                        else:
                            in_section = False
                            location['options'] = location_options
                            locations.append(location)
                            location = {}
                            location_options = {}
                    # found 'end' section marker
                    elif l.find('}') > -1:
                        in_section = False

        return servers

    def get_upstreams(self):
        """
        Gets all 'upstream' sections
        
        returns: Dict of upstream options (as separate Dict) with values

        Example:

        s = get_upstreams()

        >>> s[0]
        {'name': 'my_upstream', 'options': [{'server': ['127.0.0.3:8001']}]}

        """
        self._log.debug('Parsing upstream sections...')
        f = open(self.__filename, 'r')
        cfg = f.read()
        f.close()
        # list for all 'upstream' sections found
        upstreams = []
        # options for 'upstream' section
        upstream = {}
        upstream_options = []
        current_upstream_options = {}
        # loop through and gather options
        in_upstream_section = False
        subsection_count = 0
        for l in cfg.split('\n'):
            # skip commented sections and blank lines
            if not l.strip().startswith('#'):
                if l.strip() != '':
                    # parse options
                    if l.find('{') > -1 and l.find('upstream') > -1 and subsection_count == 0:
                        in_upstream_section = True
                        upstream_name = l.split(None, 1)[-1].replace('{', '').strip()
                        upstream['name'] = upstream_name
                        self._log.debug('Found upstream section: %s' % (upstream_name))
                    elif l.find('{') == -1 and in_upstream_section and subsection_count == 0:
                        # check for final semi-colon
                        if l.find('}') == -1:
                            # remove semi-colons and parse
                            op = l.replace(';','').split(None, 1)
                            current_upstream_options[op[0]] = op[1:]
                            upstream_options.append(current_upstream_options)
                            self._log.debug('Added upstream option: %s: %s' % (op[0], op[1:]))
                        else:
                            in_upstream_section = False
                            upstream['options'] = upstream_options
                            upstreams.append(upstream)
                            upstream = {}
                            upstream_options = []
                            current_upstream_options = {}
                    # found 'start' section tag; mark and ignore contents
                    elif l.find('{') > -1 and in_upstream_section:
                        subsection_count += 1
                    # found 'end' section marker
                    elif l.find('}') > -1 and in_upstream_section:
                        subsection_count -= 1

        return upstreams

class NginxConfig(object):
    """
    Manages Nginx configurations

    """
    def __init__(self, filename=None):
        self._log = logging.getLogger('NginxConfig')
        if not filename:
            self._log.error('You must specify a config filename...')
            return
        # check for filename; if doesn't exist, create blank config
        if not os.path.exists(filename):
            self._log.warning('Configuration file %s does not exist; creating' % (filename))
            f = open(filename, 'w')
            f.write('')
            f.close()
        self.__filename = filename
        self.__global = {}
        self.__http = {}
        self.__servers = {}
        self.__upstreams = {}
        self.__parser = NginxConfigParser(self.__filename)
        # load the configuration
        self._load_config()
    
    # accessors
    def get_filename(self): return self.__filename
    def get_global(self): return self.__global
    def get_http(self): return self.__http
    def get_servers(self): return self.__servers
    def get_upstreams(self): return self.__upstreams

    def _load_config(self):
        self.__global = self.__parser.get_global()
        self.__http = self.__parser.get_http()
        self.__servers = self.__parser.get_servers()
        self.__upstreams = self.__parser.get_upstreams()
    
