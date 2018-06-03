import os
import sys
import unittest
from functools import partial

hdr = {"User-Agent":"Mozilla/5.0"}

def hello(*args):
    print('hello: {}'.format(args[-2]))
    r = args[-1]
    print(r.html)
    print(r.charset)
    print(r.content_encoding)
    print(r.content_type)
    print(r.info)
    
def hello_world(*args):
    print('hello_world: {}'.format(args[-2]))
    r = args[-1]
    print(r.html)
    print(r.charset)
    print(r.content_encoding)
    print(r.content_type)
    print(r.info)
    
def hello_world_new(*args):
    print('hello_world new: {}'.format(args[-2]))
    r = args[-1]
    #print(r.html)
    print(r.charset)
    print(r.content_encoding)
    print(r.content_type)
    print(r.info)

class TestVinanti(unittest.TestCase):
    
    def test_gzip(self):
        vnt = Vinanti(block=False, log=False, hdrs=hdr)
        vnt.get('https://httpbin.org/gzip', onfinished=hello)
        vnt.get('https://httpbin.org/gzip', onfinished=hello, out='/tmp/gzip.html')
        
    def test_binary(self):
        vnt = Vinanti(block=False, log=False, hdrs=hdr)
        vnt.get('https://httpbin.org/get', onfinished=hello_world, binary=True)
        vnt.post('https://httpbin.org/post', data={'hello':'world'}, onfinished=hello_world, binary=True)
        
    def test_charset(self):
        vnt = Vinanti(block=False, log=False, hdrs=hdr)
        vnt.get('https://www.google.com', onfinished=hello_world_new, charset='ISO-8859-1')
        vnt.get('https://www.duckduckgo.com', onfinished=hello_world_new, charset='ISO-8859-1')
    
    def test_gzip_aio(self):
        vnt = Vinanti(block=False, log=False, hdrs=hdr, backend='aiohttp')
        vnt.get('https://httpbin.org/gzip', onfinished=hello)
        vnt.get('https://httpbin.org/gzip', onfinished=hello, out='/tmp/gzip_aio.html')
    
    def test_binary_aio(self):
        vnt = Vinanti(block=False, log=False, hdrs=hdr, backend='aiohttp')
        vnt.get('https://httpbin.org/get', onfinished=hello_world, binary=True)
        vnt.post('https://httpbin.org/post', data={'hello':'world'}, onfinished=hello_world, binary=True)
        
    def test_charset_aio(self):
        vnt = Vinanti(block=False, log=False, hdrs=hdr, backend='aiohttp')
        vnt.get('https://www.google.com', onfinished=hello_world_new, charset='ISO-8859-1')
        vnt.get('https://www.duckduckgo.com', onfinished=hello_world_new, charset='ISO-8859-1')
    
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
