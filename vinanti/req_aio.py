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

import asyncio

try:
    from vinanti.req import *
    from vinanti.log import log_function
except ImportError:
    from req import *
    from log import log_function
    
logger = log_function(__name__)


class RequestObjectAiohttp(RequestObject):
    
    def __init__(self, url, hdrs, method, kargs):
        super().__init__(url, hdrs, method, kargs)
        
    async def process_aio_request(self, session):
        func = self.get_aio_request_func(session)
        ret_obj = None
        async with func as resp:
            ret_obj = Response(self.url, method=self.method)
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
                elif self.binary:
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
        
