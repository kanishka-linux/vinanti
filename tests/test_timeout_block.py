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

import os
import sys
import unittest
from functools import partial

def hello(*args):
    future = args[-1]
    result = future.result()
    if len(args) > 3:
        new_args = args[:-3]
        print(new_args)
    if result:
        info = result.info
        if info:
            content_type = info['content-type']
        else:
            content_type = 'Not Available'
        print('{} {} {} {} error={} cookies={}'.format(
                result.url, result.status, content_type,
                result.method, result.error, result.session_cookies
                )
            )
    

class TestVinanti(unittest.TestCase):
    
    urls = [
        'http://www.yahoo.com', 'http://www.google.com',
        'http://www.duckduckgo.com',
        'http://www.yahoo.com', 'http://en.wikipedia.org'
        ]
    hdr = {'User-agent':'Mozilla/5.0'}
    
    def test_get(self):
        vnt = Vinanti(block=True)
        vnt.get(self.urls, onfinished=hello, hdrs=self.hdr, timeout=0.1)
        vnt.start()
        
    def test_head(self):
        vnt = Vinanti(block=True)
        vnt.head(self.urls, onfinished=hello, hdrs=self.hdr, timeout=0.5)
        vnt.start()
        
    def test_post(self):
        urls = ['http://httpbin.org/post', 'http://httpbin.org/post']
        vnt = Vinanti(block=True)
        vnt.post(urls, onfinished=hello, hdrs=self.hdr, data=(('moe', 'curly'), ('moe', 'larry')), timeout=1)
        vnt.start()
        
    def test_post_more(self):
        urls = ['http://httpbin.org/post', 'http://httpbin.org/post']
        vnt = Vinanti(block=True)
        vnt.post(urls, onfinished=hello, hdrs=self.hdr, data={'yotsubato':'aria','mushishi':'kino'}, timeout=0.5)
        vnt.start()
        
    def test_get_params(self):
        urls = ['http://httpbin.org/get', 'http://httpbin.org/get']
        vnt = Vinanti(block=True)
        vnt.get(urls, onfinished=hello, hdrs=self.hdr, params={'billoo':'diamond comics', 'dhruva':'raj comics'}, timeout=0.5)
        vnt.start()
        
    def test_without_hdrs(self):
        urls = ['https://news.ycombinator.com/news', 'https://github.com/']
        vnt = Vinanti(block=True)
        vnt.get(urls, onfinished=partial(hello, 'test_without_hdrs'), timeout=1.0)
        vnt.start()
        
    def test_without_callback(self):
        urls = ['https://news.ycombinator.com/news', 'https://github.com/']
        vnt = Vinanti(block=True)
        vnt.get(urls, timeout=1.0)
        vnt.start()
        
if __name__ == '__main__':
    BASEDIR, BASEFILE = os.path.split(os.path.abspath(__file__))
    parent_basedir, __ = os.path.split(BASEDIR)
    print(parent_basedir)
    sys.path.insert(0, parent_basedir)
    k_dir = os.path.join(parent_basedir, 'vinanti')
    sys.path.insert(0, k_dir)
    print(k_dir)
    from vinanti import Vinanti
    unittest.main()
