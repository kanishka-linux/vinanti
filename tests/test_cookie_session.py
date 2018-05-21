import os
import sys
import unittest
from functools import partial
import time

hdr = {"User-Agent":"Mozilla/5.0"}

def hello(*args):
    print('hello: {}'.format(args[-2]))
    r = args[-1].result()
    print(r.html)
    print(r.charset)
    print(r.content_encoding)
    print(r.content_type)
    print(r.info)
    print(r.session_cookies)
    vnt.get('http://httpbin.org/cookies', onfinished=hello_world)

def hello_world(*args):
    print('hello_world: {}'.format(args[-2]))
    r = args[-1].result()
    if 'wikipedia' not in r.url:
        print(r.html)
    print(r.charset)
    print(r.content_encoding)
    print(r.content_type)
    print(r.info)
    print(r.session_cookies)

def hello_world_new(*args):
    print('hello_world new: {}'.format(args[-2]))
    r = args[-1].result()
    print(r.charset)
    print(r.content_encoding)
    print(r.content_type)
    print(r.session_cookies)
    vnt.get('https://en.wikipedia.org', onfinished=hello_world)


class TestVinanti(unittest.TestCase):
        
    def test_session(self):
        vnt.get('https://en.wikipedia.org', onfinished=hello_world_new)
        vnt.get('http://httpbin.org/cookies/set/sessioncookie/abcdefgh', onfinished=hello)
            
        
if __name__ == '__main__':
    BASEDIR, BASEFILE = os.path.split(os.path.abspath(__file__))
    parent_basedir, __ = os.path.split(BASEDIR)
    print(parent_basedir)
    sys.path.insert(0, parent_basedir)
    k_dir = os.path.join(parent_basedir, 'vinanti')
    sys.path.insert(0, k_dir)
    print(k_dir)
    from vinanti import Vinanti
    vnt = Vinanti(block=False, log=False, hdrs=hdr, session=True)
    unittest.main()
