#!/bin/bash/env python

"""
Copyright (C) 2018 kanishka-linux kanishka.linux@gmail.com

This file is part of vinanti.

vinanti is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

vinanti is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with vinanti.  If not, see <http://www.gnu.org/licenses/>.
"""


import urllib.parse
import urllib.request


class RequestObject:
    
    def __init__(self, url, hdrs, method, kargs):
        self.url = url
        self.hdrs = hdrs
        self.kargs = kargs
        self.html = None
        self.status = None
        self.info = None
        self.url = url
        self.method = method
        self.error = None
        self.data = None
        self.timeout = self.kargs.get('timeout')
        self.__init_extra__()
    
    def __init_extra__(self):
        if not self.hdrs:
            self.hdrs = {"User-Agent":"Mozilla/5.0"}
        if not self.method:
            self.method = 'GET'
        if not self.timeout:
            self.timeout = None
        if self.method == 'POST':
            self.data = self.kargs.get('data')
            if self.data:
                self.data = urllib.parse.urlencode(self.data)
                self.data = self.data.encode('utf-8')
        elif self.method == 'GET':
            payload = self.kargs.get('params')
            if payload:
                payload = urllib.parse.urlencode(payload)
                self.url = self.url + '?' + payload
                
    def process_request(self):
        req = urllib.request.Request(self.url, data=self.data,
                                     headers=self.hdrs,
                                     method=self.method)
        try: 
            r_open = urllib.request.urlopen(req, timeout=self.timeout)
        except Exception as err:
            r_open = None
            self.error = str(err)
        ret_obj = CreateReturnObject(self, r_open)
        return ret_obj
        

class CreateReturnObject:
    
    def __init__(self, parent, req):
        self.method = parent.method
        self.error = parent.error
        if req:
            if parent.method == 'HEAD':
                self.html = 'None'
            else:
                self.html = req.read().decode('utf-8')
            self.info = req.info()
            self.url = req.geturl()
            self.status = req.getcode()
        else:
            self.html = None
            self.info = None
            self.status = None
            self.url = parent.url
