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

import shutil
import urllib.parse
import urllib.request
try:
    from vinanti.log import log_function
except ImportError:
    from log import log_function
logger = log_function(__name__)


class RequestObject:
    
    def __init__(self, url, hdrs, method, kargs):
        self.url = url
        self.hdrs = hdrs
        self.kargs = kargs
        self.html = None
        self.status = None
        self.info = None
        self.method = method
        self.error = None
        self.data = None
        self.log = kargs.get('log')
        if not self.log:
            logger.disabled = True
        self.timeout = self.kargs.get('timeout')
        self.out = self.kargs.get('out')
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
            logger.error(err)
        ret_obj = CreateReturnObject(self, r_open)
        return ret_obj
        

class CreateReturnObject:
    
    def __init__(self, parent, req):
        self.method = parent.method
        self.error = parent.error
        if req:
            self.info = req.info()
            self.url = req.geturl()
            self.status = req.getcode()
            if parent.method == 'HEAD':
                self.html = 'None'
            elif parent.out:
                with open(parent.out, 'wb') as out_file:
                    shutil.copyfileobj(req, out_file)
                self.html = 'file saved to {}'.format(parent.out)
            else:
                self.html = req.read().decode('utf-8')
        else:
            self.html = None
            self.info = None
            self.status = None
            self.url = parent.url
