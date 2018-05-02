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

import asyncio
import urllib.parse
import urllib.request
from functools import partial
from threading import Thread
from collections import OrderedDict

try:
    from vinanti.req import RequestObject
except ImportError:
    from req import RequestObject

class Vinanti:
    
    def __init__(self, backend=None, block=None):
        if backend is None:
            self.backend = 'urllib'
        else:
            self.backend = backend
        if block is None:
            self.block = True
        else:
            self.block = block
        self.loop = asyncio.get_event_loop()
        self.tasks = OrderedDict()
        self.loop_nonblock_list = []
        
    def clear(self):
        self.tasks.clear()
        self.loop_nonblock_list.clear()
    
    def __build_tasks__(self, urls, method, onfinished=None, hdrs=None, options_dict=None):
        self.tasks.clear()
        if options_dict is None:
            options_dict = {}
        if not isinstance(urls, list):
            urls = [urls]
        for url in urls:
            task_list = [url, onfinished, hdrs, method, options_dict]
            length = len(self.tasks)
            self.tasks.update({length:task_list})
            
    def get(self, urls, onfinished=None, hdrs=None, **kargs):
        self.__build_tasks__(urls, 'GET', onfinished, hdrs, kargs)
    
    def post(self, urls, onfinished=None, hdrs=None, **kargs):
        self.__build_tasks__(urls, 'POST', onfinished, hdrs, kargs)
        
    def head(self, urls, onfinished=None, hdrs=None, **kargs):
        self.__build_tasks__(urls, 'HEAD', onfinished, hdrs, kargs)
    
    def add(self, urls, onfinished=None, hdrs=None, method=None, **kargs):
        if method is None:
            method = 'GET'
        if isinstance(urls, str):
            task_list = [urls, onfinished, hdrs, method, kargs]
            length = len(self.tasks)
            self.tasks.update({length:task_list})
    
    def __start_non_block_loop__(self, tasks_dict, loop):
        asyncio.set_event_loop(loop)
        tasks = []
        for i in tasks_dict:
            url, onfinished, hdrs, method, kargs = tasks_dict[i]
            tasks.append(asyncio.ensure_future(self.__start_fetching__(url, onfinished, hdrs, i, loop, method, kargs))) 
        loop.run_until_complete(asyncio.gather(*tasks))
        
    def start(self):
        if self.block:
            self.__event_loop__(self.tasks)
        else:
            new_loop = asyncio.new_event_loop()
            loop_thread = Thread(target=self.__start_non_block_loop__, args=(self.tasks, new_loop))
            self.loop_nonblock_list.append(loop_thread)
            self.loop_nonblock_list[len(self.loop_nonblock_list)-1].start()
            
    def __event_loop__(self, tasks_dict):
        tasks = []
        for i in tasks_dict:
            url, onfinished, hdrs, method, kargs = tasks_dict[i]
            tasks.append(asyncio.ensure_future(self.__start_fetching__(url, onfinished, hdrs, i, self.loop, method, kargs))) 
        self.loop.run_until_complete(asyncio.gather(*tasks))
    
    def __get_request__(self, url, hdrs, method, kargs):
        req_obj = None
        if self.backend == 'urllib':
            req = RequestObject(url, hdrs, method, kargs)
            req_obj = req.process_request()
        return req_obj
    
    async def __start_fetching__(self, url, onfinished, hdrs, task_num, loop, method, kargs):
        future = loop.run_in_executor(None, self.__get_request__, url, hdrs, method, kargs)
        if onfinished:
            future.add_done_callback(partial(onfinished, task_num, url))
        response = await future
