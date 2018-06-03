import os
import sys
import time
import unittest
from functools import partial

hdr = {"User-Agent":"Mozilla/5.0"}

def hello(*args):
    print('hello: {} {}'.format(args[-2], time.time() - ytm))
    
def namaste(*args):
    print('namaste: {} {}'.format(args[-2], time.time() - ytm))
    
def konichiwa(*args):
    print('konichiwa: {} {}'.format(args[-2], time.time() - ytm))
    
def hello_aio(*args):
    print('hello_aio: {} {}'.format(args[-2], time.time() - ytm))
    
def namaste_aio(*args):
    print('namaste_aio: {} {}'.format(args[-2], time.time() - ytm))
    
def konichiwa_aio(*args):
    print('konichiwa_aio: {} {}'.format(args[-2], time.time() - ytm))
    
ytm = time.time()

class TestVinanti(unittest.TestCase):
    
    def test_wait_noblock(self):
        vnt = Vinanti(block=False, log=False, hdrs=hdr, wait=1.0)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
    
    def test_wait_aio(self):
        vnt = Vinanti(block=False, log=False, hdrs=hdr, wait=2.0, backend='aiohttp')
        vnt.get('http://www.google.com',onfinished=hello_aio)
        vnt.get('http://www.google.com',onfinished=hello_aio)
        vnt.get('http://www.google.com',onfinished=hello_aio)
        vnt.get('http://www.google.com',onfinished=hello_aio)
        vnt.get('http://www.google.com',onfinished=hello_aio)
        vnt.get('http://www.google.com',onfinished=hello_aio)
        vnt.get('http://www.google.com',onfinished=hello_aio)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa_aio)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa_aio)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa_aio)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa_aio)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa_aio)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa_aio)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa_aio)
        vnt.get('http://www.wikipedia.org',onfinished=namaste_aio)
        vnt.get('http://www.wikipedia.org',onfinished=namaste_aio)
        vnt.get('http://www.wikipedia.org',onfinished=namaste_aio)
        vnt.get('http://www.wikipedia.org',onfinished=namaste_aio)
        vnt.get('http://www.wikipedia.org',onfinished=namaste_aio)
        vnt.get('http://www.wikipedia.org',onfinished=namaste_aio)
        vnt.get('http://www.wikipedia.org',onfinished=namaste_aio)
    
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
