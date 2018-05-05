"""
Copyright (C) 2018 kanishka-linux kanishka.linux@gmail.com

This file is part of vinanti.

vinanti is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

vinanti is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with vinanti.  If not, see <http://www.gnu.org/licenses/>.
"""

import time
import shutil
import base64
import urllib.parse
import urllib.request
#from urllib.parse import urlparse
try:
    from vinanti.log import log_function
    from vinanti.formdata import Formdata
except ImportError:
    from log import log_function
    from formdata import Formdata
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
        self.wait = kargs.get('wait')
        self.proxies = kargs.get('proxies')
        self.auth = kargs.get('auth')
        self.files = kargs.get('files')
        self.session_object = kargs.get('session')
        if not self.log:
            logger.disabled = True
        self.timeout = self.kargs.get('timeout')
        self.out = self.kargs.get('out')
        self.__init_extra__()
    
    def __init_extra__(self):
        self.data_old = None
        if self.wait:
            logger.debug('Waiting for {} seconds: {}'.format(self.wait, self.url))
        if not self.hdrs:
            self.hdrs = {"User-Agent":"Mozilla/5.0"}
        if not self.method:
            self.method = 'GET'
        if not self.timeout:
            self.timeout = None
        if self.method == 'POST':
            self.data = self.kargs.get('data')
            if self.data:
                self.data_old = self.data
                self.data = urllib.parse.urlencode(self.data)
                self.data = self.data.encode('utf-8')
        elif self.method == 'GET':
            payload = self.kargs.get('params')
            if payload:
                payload = urllib.parse.urlencode(payload)
                self.url = self.url + '?' + payload
        if self.files:
            if self.data:
                mfiles = Formdata(self.data_old, self.files)
            else:
                mfiles = Formdata({}, self.files)
            data, hdr = mfiles.create_content()
            for key, value in hdr.items():
                self.hdrs.update({key:value})
            self.data = data
        
    def process_request(self):
        opener = None
        if self.wait:
            time.sleep(self.wait)
        if self.proxies:
            opener = self.add_proxy()
        req = urllib.request.Request(self.url, data=self.data,
                                     headers=self.hdrs,
                                     method=self.method)
        if self.auth:
            req = self.add_basic_auth(req)
        try: 
            if opener:
                r_open = opener.open(req, timeout=self.timeout)
            else:
                r_open = urllib.request.urlopen(req, timeout=self.timeout)
        except Exception as err:
            r_open = None
            self.error = str(err)
            logger.error(err)
        ret_obj = CreateReturnObject(self, r_open)
        return ret_obj
    
    def add_basic_auth(self, req):
        credentials = '{}:{}'.format(self.auth[0], self.auth[1])
        encoded_credentials = base64.b64encode(bytes(credentials, 'utf-8'))
        req.add_header('Authorization', 'Basic {}'.format(encoded_credentials.decode('utf-8')))
        return req
    
    def add_proxy(self):
        logger.info('proxies {}'.format(self.proxies))
        if self.url.startswith('http'):
            http_handler = urllib.request.HTTPHandler()
        else:
            http_handler = urllib.request.HTTPSHandler()
        proxy_handler = urllib.request.ProxyHandler(self.proxies)
        opener = urllib.request.build_opener(http_handler, proxy_handler)
        return opener
        
        
class CreateReturnObject:
    
    def __init__(self, parent, req):
        self.method = parent.method
        self.error = parent.error
        self.session_cookies = None
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
            self.set_session_cookies()
        else:
            self.html = None
            self.info = None
            self.status = None
            self.url = parent.url
    
    def set_session_cookies(self):
        #o = urlparse(self.url)
        for i in self.info.walk():
            cookie_list = i.get_all('set-cookie')
            cookie_jar = []
            if cookie_list:
                for i in cookie_list:
                    cookie = i.split(';')[0]
                    cookie_jar.append(cookie)
                if cookie_jar:
                    cookies = ';'.join(cookie_jar)
                    self.session_cookies = cookies
        
