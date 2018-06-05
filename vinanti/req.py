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

import re
import ssl
import gzip
import time
import shutil
import base64
import asyncio
import urllib.parse
import urllib.request
import http.cookiejar
from io import StringIO, BytesIO

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
        self.auth_digest = kargs.get('auth_digest')
        self.files = kargs.get('files')
        self.binary = kargs.get('binary')
        self.charset = kargs.get('charset')
        self.session = kargs.get('session')
        self.verify = kargs.get('verify')
        if not self.log:
            logger.disabled = True
        self.timeout = self.kargs.get('timeout')
        self.out = self.kargs.get('out')
        self.__init_extra__()
    
    def __init_extra__(self):
        self.data_old = None
        if not self.hdrs:
            self.hdrs = {"User-Agent":"Mozilla/5.0"}
        if not self.method:
            self.method = 'GET'
        if not self.timeout:
            self.timeout = None
        if self.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
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
        cj = None
        if self.verify is False:
            opener = self.handle_https_context(opener, False)
        if self.proxies:
            opener = self.add_proxy(opener)
        if self.session:
            opener, cj = self.enable_cookies(opener)
            
        req = urllib.request.Request(self.url, data=self.data,
                                     headers=self.hdrs,
                                     method=self.method)
        if self.auth:
            opener = self.add_http_auth(self.auth, 'basic', opener)
        elif self.auth_digest:
            opener = self.add_http_auth(self.auth_digest, 'digest', opener)
        try: 
            if opener:
                r_open = opener.open(req, timeout=self.timeout)
            else:
                r_open = urllib.request.urlopen(req, timeout=self.timeout)
        except Exception as err:
            r_open = None
            self.error = str(err)
            logger.error(err)
        ret_obj = ResponseObject(self, r_open, cj)
        return ret_obj
        
    async def process_aio_request(self, session):
        func = self.get_aio_request_func(session)
        ret_obj = None
        async with func as resp:
            ret_obj = ResponseObject(self, None, None, 'aiohttp')
            ret_obj.info = resp.headers
            text = None
            if self.method != 'HEAD':
                if self.out:
                    with open(self.out, 'wb') as fd:
                        while True:
                            chunk = await resp.content.read(1024)
                            if not chunk:
                                break
                            fd.write(chunk)
                        text = 'file saved to {}'.format(self.out)
                else:
                    if self.binary:
                        text = await resp.read()
                    elif self.charset:
                        text = await resp.text(encoding=self.charset)
                    else:
                        text = await resp.text(encoding='utf-8')
            ret_obj.html = text
            ret_obj.status = resp.status
            ret_obj.content_type = ret_obj.info.get('content-type')
            ret_obj.url = str(resp.url)
            cj_arr = []
            for c in session.cookie_jar:
                cj_arr.append('{}={}'.format(c.key, c.value))
            ret_obj.session_cookies = ';'.join(cj_arr)
        return ret_obj
        
    def get_aio_request_func(self, session):
        if self.method == 'GET':
            func = session.get
        elif self.method == 'POST':
            func = session.post
        elif self.method == 'PUT':
            func = session.put
        elif self.method == 'PATCH':
            func = session.patch
        elif self.method == 'DELETE':
            func = session.delete
        elif self.method == 'HEAD':
            func = session.head
        elif self.method == 'OPTIONS':
            func = session.options
        if self.timeout is None:
            self.timeout = 300
        if self.verify is False:
            verify = False
        else:
            verify = True
        http_proxy = None
        if self.proxies:
            http_proxy = self.proxies.get('http')
            if not http_proxy:
                http_proxy = self.proxies.get('https')
        new_func = func(self.url, headers=self.hdrs, timeout=self.timeout,
                        ssl=verify, proxy=http_proxy, data=self.data)
        return new_func
                
    def add_http_auth(self, auth_tuple, auth_type, opener=None):
        logger.info(auth_type)
        usr = auth_tuple[0]
        passwd = auth_tuple[1]
        if len(auth_tuple) == 2:
            realm = None
        elif len(auth_tuple) == 3:
            realm = auth_tuple[2]
        password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(realm, self.url, usr, passwd)
        if auth_type == 'basic':
            auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
        else:
            auth_handler = urllib.request.HTTPDigestAuthHandler(password_manager)
        if opener:
            logger.info('Adding Handle to Existing Opener')
            opener.add_handler(auth_handler)
        else:
            opener = urllib.request.build_opener(auth_handler)
        return opener
        """
        credentials = '{}:{}'.format(usr, passwd)
        encoded_credentials = base64.b64encode(bytes(credentials, 'utf-8'))
        req.add_header('Authorization', 'Basic {}'.format(encoded_credentials.decode('utf-8')))
        return req
        """
    
    def handle_https_context(self, opener, verify):
        context = ssl.create_default_context()
        if verify is False:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        https_handler = urllib.request.HTTPSHandler(context=context)
        if opener:
            logger.info('Adding HTTPS Handle to Existing Opener')
            opener.add_handler(https_handler)
        else:
            opener = urllib.request.build_opener(https_handler)
        return opener
    
    def enable_cookies(self, opener):
        cj = http.cookiejar.CookieJar()
        cookie_handler = urllib.request.HTTPCookieProcessor(cj)
        if opener:
            logger.info('Adding Cookie Handle to Existing Opener')
            opener.add_handler(cookie_handler)
        else:
            opener = urllib.request.build_opener(cookie_handler)
        return opener, cj
        
    def add_proxy(self, opener):
        logger.info('proxies {}'.format(self.proxies))
        proxy_handler = urllib.request.ProxyHandler(self.proxies)
        if opener:
            logger.info('Adding Proxy Handle to Existing Opener')
            opener.add_handler(proxy_handler)
        else:
            opener = urllib.request.build_opener(proxy_handler)
        return opener
        
        
class ResponseObject:
    
    def __init__(self, parent=None, req=None, cj=None, backend='urllib'):
        if parent:
            self.method = parent.method
            self.error = parent.error
        else:
            self.method = None
            self.error = None
        self.session_cookies = None
        self.charset = None
        self.html = None
        if req and backend != 'aiohttp':
            self.set_information(req, parent)
            self.set_session_cookies(cj)
        else:
            self.info = None
            self.status = None
            if parent:
                self.url = parent.url
            else:
                self.url = None
            self.content_type = None
            self.content_encoding = None
            
    def set_information(self, req, parent):
        self.info = req.info()
        self.url = req.geturl()
        self.status = req.getcode()
        self.content_encoding = self.info.get('content-encoding')
        self.content_type = self.info.get('content-type')
        
        if not self.content_type:
            self.content_type = 'Not Available'
        else:
            charset_s = re.search('charset[^;]*', self.content_type.lower())
            if charset_s:
                charset_t = charset_s.group()
                charset_t = charset_t.replace('charset=', '')
                self.charset = charset_t.strip()
        if parent.charset:
            self.charset = parent.charset
        
        self.readable_format = [
            'text/plain', 'text/html', 'text/css', 'text/javascript',
            'application/xhtml+xml', 'application/xml', 'application/json',
            'application/javascript', 'application/ecmascript'
            ]
        human_readable = False
        for i in self.readable_format:
            if i in self.content_type.lower():
                human_readable = True
                break
                
        dstorage = None
        if self.content_encoding == 'gzip':
            try:
                storage = BytesIO(req.read())
                dstorage = gzip.GzipFile(fileobj=storage)
            except Exception as err:
                logger.error(err)
                
        if parent.method == 'HEAD':
            self.html = 'None'
        elif parent.out:
            with open(parent.out, 'wb') as out_file:
                if dstorage is None:
                    shutil.copyfileobj(req, out_file)
                else:
                    shutil.copyfileobj(dstorage, out_file)
            self.html = 'file saved to {}'.format(parent.out)
        else:
            self.read_html(parent, req, dstorage, human_readable)
        
            
    def read_html(self, parent, req, dstorage, human_readable):
        try:
            decoding_required = False
            if dstorage is None and human_readable and not parent.binary:
                self.html = req.read()
                decoding_required = True
            elif dstorage and human_readable and not parent.binary:
                self.html = dstorage.read()
                decoding_required = True
            elif parent.binary:
                self.html = req.read()
            else:
                self.html = 'not human readable content: content-type is {}'.format(self.content_type)
            if decoding_required:
                if self.charset:
                    try:
                        self.html = self.html.decode(self.charset)
                    except Exception as err:
                        logger.error(err)
                        self.html = self.html.decode('utf-8')
                else:
                    self.html = self.html.decode('utf-8')
        except Exception as err:
            logger.error(err)
            self.html = str(err)
    
    def set_session_cookies(self, cj):
        if cj:
            cj_arr = []
            for i in cj:
                cj_arr.append('{}={}'.format(i.name, i.value))
            self.session_cookies = ';'.join(cj_arr)
        else:
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
    
